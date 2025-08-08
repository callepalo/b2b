from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator
from config.supabase import get_supabase

router = APIRouter(prefix="/productos", tags=["productos"])

# Modelos Pydantic para Productos
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: float = Field(..., gt=0, description="El precio debe ser mayor que cero")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    categoria_id: str = Field(..., description="ID de la categoría a la que pertenece el producto")

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: str  # Cambiado de int a str para soportar UUID

    class Config:
        from_attributes = True

# Endpoints
@router.get("", response_model=List[Producto], response_model_exclude_none=True)
async def obtener_productos(
    categoria_id: Optional[str] = Query(None, description="Filtrar por ID de categoría")
):
    """Obtener todos los productos, opcionalmente filtrados por categoría"""
    try:
        supabase = get_supabase()
        query = supabase.table('productos').select('*')
        
        if categoria_id:
            query = query.eq('categoria_id', categoria_id)
        
        response = query.execute()
        
        # Asegurarse de que siempre devolvemos una lista
        if not response.data:
            return []
            
        return response.data
    except Exception as e:
        print(f"Error en obtener_productos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los productos: {str(e)}"
        )

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
    
    # Verificar que la categoría exista
    categoria = supabase.table('categorias').select('id').eq('id', producto.categoria_id).execute()
    if not categoria.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No existe una categoría con ID {producto.categoria_id}"
        )
    
    # Crear el producto
    response = supabase.table('productos').insert(producto.dict()).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el producto"
        )
    
    # Obtener el producto recién creado con sus relaciones
    nuevo_producto = supabase.table('productos').select('*, categorias(*)').eq('id', response.data[0]['id']).execute()
    return nuevo_producto.data[0] if nuevo_producto.data else response.data[0]

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
