from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from .auth_utils import get_current_user, CurrentUser

router = APIRouter()

class ProfileMe(BaseModel):
    id: str
    email: Optional[str] = None
    role: Optional[str] = None

@router.get("/profiles/me", response_model=ProfileMe)
async def get_me(user: CurrentUser = Depends(get_current_user)):
    return ProfileMe(id=user.id, email=user.email, role=user.role)
