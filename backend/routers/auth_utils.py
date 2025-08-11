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
        # Supabase tokens include an 'aud' claim (e.g., 'authenticated').
        # We are not setting an expected audience here, so disable audience verification.
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM], options={"verify_aud": False})
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature (check SUPABASE_JWT_SECRET)")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")

    user_id = payload.get('sub') or payload.get('user_id') or payload.get('uid')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    # Cargar perfil con varias estrategias: id, user_id, email
    sb = get_supabase()
    email_claim = payload.get('email')
    # 1) Buscar por id (lo esperado si id = auth.users.id)
    sel = 'id,email,role,user_id'
    prof = sb.table('profiles').select(sel).eq('id', user_id).limit(1).execute().data or []
    if not prof:
        # 2) Algunos esquemas usan columna user_id
        prof = sb.table('profiles').select(sel).eq('user_id', user_id).limit(1).execute().data or []
    if not prof and email_claim:
        # 3) Fallback por email si existe
        prof = sb.table('profiles').select(sel).eq('email', email_claim).limit(1).execute().data or []
    if not prof:
        # Placeholder si no existe registro
        return CurrentUser(user_id=user_id, email=email_claim, role=None)
    p = prof[0]
    return CurrentUser(user_id, p.get('email') or email_claim, p.get('role'))


def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user
