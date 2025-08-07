from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from datetime import datetime

# Configuración de Supabase
from config.supabase import get_supabase

app = FastAPI(
    title="Dulpromax API",
    description="API para el sistema de Dulpromax",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dulpromax.netlify.app",
        "http://localhost:8000"  # Para desarrollo local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para Productos
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0, description="El precio debe ser mayor que cero")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    categoria: Optional[str] = None
    imagen_url: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: str
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    environment: str

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API de Dulpromax!"}

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check() -> HealthCheckResponse:
    """
    Endpoint para verificar el estado de la API.
    Devuelve el estado actual, versión y entorno de la aplicación.
    """
    return HealthCheckResponse(
        status="OK",
        version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("ENVIRONMENT", "production")
    )

# Dependencia para obtener la instancia de Supabase
def get_supabase_client():
    return get_supabase(use_service_role=True)

# Endpoints para Productos
@app.get("/productos", response_model=List[Producto])
async def listar_productos(supabase: Client = Depends(get_supabase_client)):
    """
    Obtiene todos los productos del catálogo.
    """
    try:
        response = supabase.table('productos').select('*').execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}"
        )

@app.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    producto: ProductoCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Crea un nuevo producto en el catálogo.
    """
    try:
        # Insertar el producto en Supabase
        response = supabase.table('productos').insert(producto.dict()).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear el producto"
            )
            
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto: {str(e)}"
        )

@app.get("/productos/{producto_id}", response_model=Producto)
async def obtener_producto(
    producto_id: str,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Obtiene un producto por su ID.
    """
    try:
        response = supabase.table('productos').select('*').eq('id', producto_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
            
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el producto: {str(e)}"
        )

@app.put("/productos/{producto_id}", response_model=Producto)
async def actualizar_producto(
    producto_id: str,
    producto: ProductoCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Actualiza un producto existente.
    """
    try:
        # Verificar si el producto existe
        existe = supabase.table('productos').select('id').eq('id', producto_id).execute()
        if not existe.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        # Actualizar el producto
        response = supabase.table('productos').update(
            producto.dict(exclude_unset=True)
        ).eq('id', producto_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo actualizar el producto"
            )
            
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el producto: {str(e)}"
        )

@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(
    producto_id: str,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Elimina un producto del catálogo.
    """
    try:
        # Verificar si el producto existe
        existe = supabase.table('productos').select('id').eq('id', producto_id).execute()
        if not existe.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        # Eliminar el producto
        supabase.table('productos').delete().eq('id', producto_id).execute()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el producto: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
