import os
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase_client import get_supabase

JWT_SECRET_ENV = "SUPABASE_JWT_SECRET"
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer(auto_error=False)

class CurrentUser:
    def __init__(self, user_id: str, email: Optional[str], role: Optional[str]):
        self.id = user_id
        self.email = email
        self.role = role


def get_current_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> CurrentUser:
    if not creds or not creds.scheme.lower() == 'bearer':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

    token = creds.credentials
    secret = os.getenv(JWT_SECRET_ENV)
    if not secret:
        raise HTTPException(status_code=500, detail="Server misconfigured: SUPABASE_JWT_SECRET missing")

    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get('sub') or payload.get('user_id') or payload.get('uid')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    # Cargar perfil
    sb = get_supabase()
    prof = sb.table('profiles').select('id,email,role').eq('id', user_id).limit(1).execute().data or []
    if not prof:
        # Crear placeholder si no existe (raro si trigger está activo)
        email = payload.get('email')
        return CurrentUser(user_id=user_id, email=email, role=None)
    p = prof[0]
    return CurrentUser(user_id, p.get('email'), p.get('role'))


def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user
