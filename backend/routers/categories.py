from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import uuid
from supabase_client import get_supabase
from .auth_utils import require_admin

router = APIRouter()

# Modelos Pydantic
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    slug: str
    parent_id: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: str
    image_url: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    data: List[Category]
    total: int

@router.get("/categories")
async def get_categories():
    """Obtener todas las categorías"""
    sb = get_supabase()
    resp = sb.table('categories').select('*', count='exact').order('sort_order').execute()
    data = resp.data or []
    total = resp.count if hasattr(resp, 'count') else len(data)
    return {"data": data, "total": total}

@router.get("/categories/{category_id}")
async def get_category(category_id: str):
    """Obtener una categoría específica"""
    sb = get_supabase()
    resp = sb.table('categories').select('*').eq('id', category_id).limit(1).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return data[0]

@router.post("/categories", dependencies=[Depends(require_admin)])
async def create_category(category: CategoryCreate):
    """Crear una nueva categoría"""
    sb = get_supabase()
    payload = {
        **category.model_dump(),
        # id/created_at/updated_at pueden venir por default desde la DB
        "is_active": True,
        "sort_order": 0,
    }
    resp = sb.table('categories').insert(payload).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=500, detail="No se pudo crear la categoría")
    return data[0]

@router.put("/categories/{category_id}", dependencies=[Depends(require_admin)])
async def update_category(category_id: str, category: CategoryCreate):
    """Actualizar una categoría existente"""
    sb = get_supabase()
    payload = category.model_dump()
    resp = sb.table('categories').update(payload).eq('id', category_id).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return data[0]

@router.delete("/categories/{category_id}", dependencies=[Depends(require_admin)])
async def delete_category(category_id: str):
    """Eliminar una categoría"""
    sb = get_supabase()
    resp = sb.table('categories').delete().eq('id', category_id).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada exitosamente", "data": data[0]}
