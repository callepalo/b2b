from fastapi import APIRouter, HTTPException, Request, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import jwt
from supabase import Client
from supabase_client import get_supabase

router = APIRouter()

# Helper: admin auth
class AdminContext(BaseModel):
    user_id: str
    role: str

async def require_admin(request: Request, sb: Client = Depends(get_supabase)) -> AdminContext:
    auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization Bearer token")
    token = auth_header.split(" ", 1)[1].strip()
    try:
        # Decode without verification to read 'sub' (Supabase user id)
        payload = jwt.decode(token, options={"verify_signature": False, "verify_aud": False})
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token without sub")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    # Fetch profile to check role
    prof = sb.table('profiles').select('id, role').eq('id', user_id).limit(1).execute()
    data = (prof.data or []) if hasattr(prof, 'data') else prof.get('data', [])
    if not data:
        raise HTTPException(status_code=403, detail="Profile not found")
    role = data[0].get('role')
    if role != 'admin':
        raise HTTPException(status_code=403, detail="Admin role required")
    return AdminContext(user_id=user_id, role=role)

# Pydantic models
class SegmentPriceIn(BaseModel):
    product_id: str = Field(...)
    user_type_id: str = Field(...)
    price: float = Field(..., ge=0)

class SegmentPriceOut(SegmentPriceIn):
    id: str

class OverridePriceIn(BaseModel):
    product_id: str = Field(...)
    organization_id: str = Field(...)
    price: float = Field(..., ge=0)

class OverridePriceOut(OverridePriceIn):
    id: str

# Segment Prices CRUD
@router.get("/admin/pricing/segments", response_model=List[SegmentPriceOut])
async def list_segment_prices(
    product_id: Optional[str] = None,
    user_type_id: Optional[str] = None,
    admin: AdminContext = Depends(require_admin),
    sb: Client = Depends(get_supabase),
):
    query = sb.table('segment_prices').select('*')
    if product_id:
        query = query.eq('product_id', product_id)
    if user_type_id:
        query = query.eq('user_type_id', user_type_id)
    resp = query.execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data', [])
    return data or []

@router.post("/admin/pricing/segments", response_model=SegmentPriceOut)
async def create_segment_price(payload: SegmentPriceIn, admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('segment_prices').insert(payload.model_dump()).select('*').single().execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data')
    if not data:
        raise HTTPException(status_code=500, detail="Failed to create segment price")
    return data

@router.put("/admin/pricing/segments/{id}", response_model=SegmentPriceOut)
async def update_segment_price(id: str, payload: SegmentPriceIn, admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('segment_prices').update(payload.model_dump()).eq('id', id).select('*').single().execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data')
    if not data:
        raise HTTPException(status_code=404, detail="Segment price not found")
    return data

@router.delete("/admin/pricing/segments/{id}")
async def delete_segment_price(id: str, admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('segment_prices').delete().eq('id', id).execute()
    return {"deleted": True}

# Customer Overrides CRUD
@router.get("/admin/pricing/overrides", response_model=List[OverridePriceOut])
async def list_overrides(
    product_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    admin: AdminContext = Depends(require_admin),
    sb: Client = Depends(get_supabase),
):
    query = sb.table('customer_overrides').select('*')
    if product_id:
        query = query.eq('product_id', product_id)
    if organization_id:
        query = query.eq('organization_id', organization_id)
    resp = query.execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data', [])
    return data or []

@router.post("/admin/pricing/overrides", response_model=OverridePriceOut)
async def create_override(payload: OverridePriceIn, admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('customer_overrides').insert(payload.model_dump()).select('*').single().execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data')
    if not data:
        raise HTTPException(status_code=500, detail="Failed to create override")
    return data

@router.put("/admin/pricing/overrides/{id}", response_model=OverridePriceOut)
async def update_override(id: str, payload: OverridePriceIn, admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('customer_overrides').update(payload.model_dump()).eq('id', id).select('*').single().execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data')
    if not data:
        raise HTTPException(status_code=404, detail="Override not found")
    return data

@router.delete("/admin/pricing/overrides/{id}")
async def delete_override(id: str, admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('customer_overrides').delete().eq('id', id).execute()
    return {"deleted": True}

# Admin metadata helpers
@router.get("/admin/user-types")
async def list_user_types(admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('user_types').select('id, name').order('name').execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data', [])
    return data or []

@router.get("/admin/organizations")
async def list_organizations(admin: AdminContext = Depends(require_admin), sb: Client = Depends(get_supabase)):
    resp = sb.table('organizations').select('id, name, user_type_id').order('name').execute()
    data = resp.data if hasattr(resp, 'data') else resp.get('data', [])
    return data or []
