from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from config.supabase import get_supabase

router = APIRouter(prefix="/productos", tags=["productos"])

# Modelos Pydantic para Productos
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0, description="El precio debe ser mayor que cero")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: str  # Cambiado de int a str para soportar UUID

    class Config:
        from_attributes = True

# Endpoints
@router.get("/", response_model=List[Producto])
async def obtener_productos():
    """Obtener todos los productos"""
    supabase = get_supabase()
    response = supabase.table('productos').select('*').execute()
    return response.data if response.data else []

@router.get("/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: str):  # Cambiado de int a str
    """Obtener un producto por ID"""
    supabase = get_supabase()
    response = supabase.table('productos').select('*').eq('id', producto_id).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    return response.data[0]

@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    supabase = get_supabase()
    
    # Verificar si ya existe un producto con el mismo nombre
    existing = supabase.table('productos').select('id').eq('nombre', producto.nombre).execute()
    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con este nombre"
        )
    
    response = supabase.table('productos').insert(producto.dict()).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el producto"
        )
    
    return response.data[0]

@router.put("/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: str, producto: ProductoCreate):  # Cambiado de int a str
    """Actualizar un producto existente"""
    supabase = get_supabase()
    
    # Verificar si el producto existe
    existing = supabase.table('productos').select('*').eq('id', producto_id).execute()
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    # Verificar si hay otro producto con el mismo nombre
    same_name = supabase.table('productos') \
        .select('id') \
        .eq('nombre', producto.nombre) \
        .neq('id', producto_id) \
        .execute()
    
    if same_name.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe otro producto con este nombre"
        )
    
    response = supabase.table('productos').update(producto.dict()).eq('id', producto_id).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el producto"
        )
    
    return response.data[0]

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(producto_id: str):  # Cambiado de int a str
    """Eliminar un producto"""
    supabase = get_supabase()
    
    # Verificar si el producto existe
    existing = supabase.table('productos').select('id').eq('id', producto_id).execute()
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    response = supabase.table('productos').delete().eq('id', producto_id).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el producto"
        )
    
    return None
