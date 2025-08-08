from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field
from config.supabase import get_supabase

router = APIRouter(prefix="/categorias", tags=["categorias"])

# Modelo Pydantic para Categorías
class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: str  # UUID
    
    class Config:
        from_attributes = True

# Endpoints para Categorías
@router.get("/", response_model=List[Categoria])
async def obtener_categorias():
    """Obtener todas las categorías"""
    supabase = get_supabase()
    response = supabase.table('categorias').select('*').order('nombre').execute()
    return response.data if response.data else []

@router.get("/{categoria_id}", response_model=Categoria)
async def obtener_categoria(categoria_id: str):
    """Obtener una categoría por ID"""
    supabase = get_supabase()
    response = supabase.table('categorias').select('*').eq('id', categoria_id).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    return response.data[0]
