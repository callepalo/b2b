from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field
from config.supabase import get_supabase

router = APIRouter(tags=["categorias"])

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
@router.get("", response_model=List[Categoria])
async def obtener_categorias():
    """Obtener todas las categorías"""
    supabase = get_supabase()
    response = supabase.table('categorias').select('*').order('nombre').execute()
    return response.data if response.data else []

@router.get("{categoria_id}", response_model=Categoria)
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

@router.post("", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def crear_categoria(categoria: CategoriaCreate):
    """Crear una nueva categoría"""
    supabase = get_supabase()
    
    # Verificar si ya existe una categoría con el mismo nombre (case insensitive)
    existing = supabase.table('categorias')\
        .select('*')\
        .ilike('nombre', categoria.nombre)\
        .execute()
    
    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con este nombre"
        )
    
    try:
        # Insertar la nueva categoría
        response = supabase.table('categorias')\
            .insert(categoria.model_dump())\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la categoría"
            )
            
        # Obtener la categoría recién creada para devolverla
        new_category = response.data[0]
        return new_category
        
    except Exception as e:
        print(f"Error al crear categoría: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la categoría: {str(e)}"
        )
