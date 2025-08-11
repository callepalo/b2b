def _base_slug(name: str) -> str:
    return (name or '').strip().lower().replace(' ', '-').replace('/', '-')

def _unique_slug(sb, base: str, exclude_id: str | None = None) -> str:
    """Ensure slug uniqueness by appending a short uuid if needed."""
    if not base:
        base = str(uuid.uuid4())[:8]
    # Check exact match first (excluding current id on updates)
    q = sb.table('products').select('id').eq('slug', base)
    if exclude_id:
        q = q.neq('id', exclude_id)
    resp = q.limit(1).execute()
    exists = bool(resp.data)
    if not exists:
        return base
    # Append short suffix
    return f"{base}-{uuid.uuid4().hex[:6]}"
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
import os
from supabase_client import get_supabase
from .auth_utils import require_admin

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
    # Campos extra para catálogo
    packs: list = []
    min_price: Optional[float] = None

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    data: List[Product]
    total: int
    page: int
    per_page: int

# Helpers
def _sync_product_price(sb, product_id: str):
    """Sincroniza products.price con el menor precio de packs activos, si existen.
    Si no hay packs activos, no cambia el precio (mantiene valor actual).
    """
    try:
        r = sb.table('product_pack_options').select('price, is_active').eq('product_id', product_id).eq('is_active', True).execute()
        rows = r.data or []
        if rows:
            min_price = min([(row.get('price') or 0) for row in rows])
            sb.table('products').update({'price': float(min_price)}).eq('id', product_id).execute()
    except Exception:
        # No elevar: no debe romper el flujo si falla la sincronización
        pass

# Packs (presentaciones por empaque)
class PackBase(BaseModel):
    pack_size: int = Field(..., ge=1, description="Cantidad por empaque, mínimo 1")
    price: float = Field(..., ge=0, description="Precio del empaque, mínimo 0")
    is_active: bool = True

class PackCreate(PackBase):
    pass

class Pack(PackBase):
    id: str
    product_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

@router.get("/products", response_model=ProductResponse)
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    mode: Optional[str] = Query(None, description="Si es 'catalog', filtra activos y expone packs activos y min_price"),
    expand: Optional[str] = Query(None, description="Lista separada por comas; soporta 'packs' para adjuntar presentaciones")
):
    """Obtener todos los productos con paginación y filtros"""
    sb = get_supabase()
    query = sb.table('products').select('*', count='exact')
    is_catalog = (mode == 'catalog')
    if is_catalog:
        query = query.eq('is_active', True)
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
    # Expandir packs y calcular min_price si se solicita (o si es catálogo)
    do_expand_packs = is_catalog or (expand and ('packs' in (expand or '').split(',')))
    if do_expand_packs:
        for item in data:
            try:
                q = sb.table('product_pack_options').select('id, pack_size, price, is_active').eq('product_id', item['id'])
                if is_catalog:
                    q = q.eq('is_active', True)
                packs = q.order('pack_size', desc=False).execute().data or []
                item['packs'] = packs
                active_prices = [float(p.get('price') or 0) for p in packs if p.get('is_active')]
                item['min_price'] = (min(active_prices) if active_prices else None)
            except Exception:
                item['packs'] = []
                item['min_price'] = None
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

@router.post("/products", response_model=Product, dependencies=[Depends(require_admin)])
async def create_product(product: ProductCreate):
    """Crear un nuevo producto"""
    sb = get_supabase()
    payload = product.model_dump()
    # Generate unique slug
    base = _base_slug(product.name)
    slug = _unique_slug(sb, base)
    payload.update({
        "slug": slug,
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

@router.put("/products/{product_id}", response_model=Product, dependencies=[Depends(require_admin)])
async def update_product(product_id: str, product: ProductCreate):
    """Actualizar un producto existente"""
    sb = get_supabase()
    payload = product.model_dump()
    # Mantener slug en sync con el nombre si cambia, asegurando unicidad (excluyendo el propio producto)
    base = _base_slug(product.name)
    slug = _unique_slug(sb, base, exclude_id=product_id)
    payload.update({
        "slug": slug,
        "short_description": (product.description[:100] if product.description else None),
    })
    resp = sb.table('products').update(payload).eq('id', product_id).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return data[0]

@router.delete("/products/{product_id}", dependencies=[Depends(require_admin)])
async def delete_product(product_id: str):
    """Eliminar un producto"""
    sb = get_supabase()
    resp = sb.table('products').delete().eq('id', product_id).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado exitosamente", "data": data[0]}

@router.post("/products/{product_id}/image", dependencies=[Depends(require_admin)])
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

# ==========================
# Packs: CRUD de presentaciones
# ==========================

@router.get("/products/{product_id}/packs", response_model=List[Pack])
async def list_product_packs(product_id: str):
    sb = get_supabase()
    resp = sb.table('product_pack_options').select('*').eq('product_id', product_id).order('pack_size', desc=False).execute()
    return resp.data or []

@router.post("/products/{product_id}/packs", response_model=Pack, dependencies=[Depends(require_admin)])
async def create_product_pack(product_id: str, pack: PackCreate):
    sb = get_supabase()
    # Asegurar que producto existe (opcional, para mejor error)
    prod = sb.table('products').select('id').eq('id', product_id).limit(1).execute().data or []
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    payload = pack.model_dump()
    payload['product_id'] = product_id
    try:
        resp = sb.table('product_pack_options').insert(payload).execute()
    except Exception as e:
        # Puede fallar por unique (product_id, pack_size)
        raise HTTPException(status_code=400, detail=f"No se pudo crear la presentación: {e}")
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=500, detail="No se pudo crear la presentación")
    # Sincronizar precio base del producto con el menor pack activo
    _sync_product_price(sb, product_id)
    return data[0]

@router.put("/products/{product_id}/packs/{pack_id}", response_model=Pack, dependencies=[Depends(require_admin)])
async def update_product_pack(product_id: str, pack_id: str, pack: PackCreate):
    sb = get_supabase()
    # Validar existencia
    exists = sb.table('product_pack_options').select('id').eq('id', pack_id).eq('product_id', product_id).limit(1).execute().data or []
    if not exists:
        raise HTTPException(status_code=404, detail="Presentación no encontrada")
    try:
        resp = sb.table('product_pack_options').update(pack.model_dump()).eq('id', pack_id).eq('product_id', product_id).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo actualizar la presentación: {e}")
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=500, detail="No se pudo actualizar la presentación")
    _sync_product_price(sb, product_id)
    return data[0]

@router.delete("/products/{product_id}/packs/{pack_id}", dependencies=[Depends(require_admin)])
async def delete_product_pack(product_id: str, pack_id: str):
    sb = get_supabase()
    resp = sb.table('product_pack_options').delete().eq('id', pack_id).eq('product_id', product_id).execute()
    data = resp.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Presentación no encontrada")
    _sync_product_price(sb, product_id)
    return {"message": "Presentación eliminada", "data": data[0]}
