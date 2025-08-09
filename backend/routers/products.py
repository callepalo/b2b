from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
import uuid
import os
from supabase_client import get_supabase

router = APIRouter()

# Modelos Pydantic
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    category_id: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str
    slug: str
    short_description: Optional[str] = None
    compare_price: Optional[float] = None
    sku: Optional[str] = None
    images: list = []
    attributes: dict = {}
    is_active: bool = True
    is_featured: bool = False
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    data: List[Product]
    total: int
    page: int
    per_page: int

@router.get("/products", response_model=ProductResponse)
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    category_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Obtener todos los productos con paginación y filtros"""
    sb = get_supabase()
    query = sb.table('products').select('*', count='exact')
    if category_id:
        query = query.eq('category_id', category_id)
    if search:
        like = f"%{search}%"
        # name ilike OR description ilike
        query = query.or_(f"name.ilike.{like},description.ilike.{like}")

    # Paginación usando range (end es inclusivo)
    start = (page - 1) * per_page
    end = start + per_page - 1
    query = query.order('created_at', desc=True).range(start, end)
    resp = query.execute()
    data = resp.data or []
    total = resp.count if hasattr(resp, 'count') else len(data)
    return {"data": data, "total": total, "page": page, "per_page": per_page}

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Obtener un producto específico"""
    sb = get_supabase()
    resp = sb.table('products').select('*').eq('id', product_id).limit(1).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return data[0]

@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    """Crear un nuevo producto"""
    sb = get_supabase()
    payload = product.model_dump()
    payload.update({
        "slug": product.name.lower().replace(" ", "-"),
        "short_description": (product.description[:100] if product.description else None),
        "compare_price": None,
        "sku": None,
        "images": [],
        "attributes": {},
        "is_active": True,
        "is_featured": False,
    })
    resp = sb.table('products').insert(payload).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=500, detail="No se pudo crear el producto")
    return data[0]

@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: ProductCreate):
    """Actualizar un producto existente"""
    sb = get_supabase()
    payload = product.model_dump()
    # Mantener slug en sync con el nombre si cambia
    payload.update({
        "slug": product.name.lower().replace(" ", "-"),
        "short_description": (product.description[:100] if product.description else None),
    })
    resp = sb.table('products').update(payload).eq('id', product_id).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return data[0]

@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """Eliminar un producto"""
    sb = get_supabase()
    resp = sb.table('products').delete().eq('id', product_id).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado exitosamente", "data": data[0]}

@router.post("/products/{product_id}/image")
async def upload_product_image(product_id: str, file: UploadFile = File(...)):
    """Subir imagen de producto a Supabase Storage y actualizar el array images."""
    sb = get_supabase()

    # Verificar que el producto exista y obtener sus imágenes actuales
    prod_resp = sb.table('products').select('id, images').eq('id', product_id).limit(1).execute()
    prod_data = prod_resp.data or []
    if not prod_data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Preparar path/nombre del archivo
    _, ext = os.path.splitext(file.filename or '')
    ext = (ext or '').lower() or '.jpg'
    key = f"{product_id}/{uuid.uuid4()}{ext}"

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Archivo vacío")

    try:
        bucket = sb.storage.from_('product-images')
        # Subir sin opciones (evita incompatibilidades de versiones)
        try:
            bucket.upload(key, content)
        except TypeError:
            # Fallback con nombres de argumentos alternos
            bucket.upload(path=key, file=content)
        public_raw = bucket.get_public_url(key)
        # Normalizar a string por si la librería retorna un objeto
        public = None
        if isinstance(public_raw, str):
            public = public_raw
        elif isinstance(public_raw, dict):
            public = public_raw.get('publicUrl') or (public_raw.get('data') or {}).get('publicUrl') or public_raw.get('signedUrl')
        if not public:
            raise RuntimeError(f"No se obtuvo URL pública válida: {public_raw}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {e}")

    # Actualizar el array de imágenes del producto
    images = prod_data[0].get('images') or []
    # Asegurar que guardamos strings (si hay objetos previos, los mantenemos y añadimos string)
    images.append(public)
    sb.table('products').update({"images": images}).eq('id', product_id).execute()

    return {"url": public, "images": images}
