from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ProductoBase(BaseModel):
    """Campos comunes para crear y actualizar un producto."""
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: float = Field(..., gt=0, description="El precio debe ser mayor que cero")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    categoria_id: Optional[str] = Field(None, description="ID de la categoría a la que pertenece el producto")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen del producto")

class ProductoCreate(ProductoBase):
    """Modelo usado al crear un producto (hereda de ProductoBase)."""
    pass

class Producto(BaseModel):
    """Modelo devuelto por la API, incluye el ID generado por Supabase."""
    id: str

    model_config = ConfigDict(from_attributes=True)

class CategoriaBase(BaseModel):
    """Campos comunes para crear y actualizar una categoría."""
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(BaseModel):
    """Modelo devuelto por la API, incluye el ID generado por Supabase."""
    id: str

    model_config = ConfigDict(from_attributes=True)
