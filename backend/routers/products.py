from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import uuid

router = APIRouter()

# Modelos Pydantic
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    category_id: str

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

# Datos de ejemplo
MOCK_PRODUCTS = [
    {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "name": "Proteína Whey 100% Natural",
        "slug": "proteina-whey-natural",
        "description": "Proteína whey de alta calidad sin aditivos artificiales",
        "short_description": "Proteína pura para tus entrenamientos",
        "price": 45000.00,
        "compare_price": 50000.00,
        "stock_quantity": 50,
        "sku": "PRO-WHEY-001",
        "category_id": "550e8400-e29b-41d4-a716-446655440001",
        "images": [{"url": "https://example.com/proteina.jpg", "alt": "Proteína Whey"}],
        "attributes": {"sabor": "vainilla", "peso": "1kg", "marca": "NaturePro"},
        "is_active": True,
        "is_featured": True,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "660e8400-e29b-41d4-a716-446655440002",
        "name": "Barra de Proteína Casera",
        "slug": "barra-proteina-casera",
        "description": "Barra energética con 15g de proteína por porción",
        "short_description": "Snack saludable y rico en proteínas",
        "price": 3500.00,
        "stock_quantity": 100,
        "sku": "BAR-PRO-001",
        "category_id": "550e8400-e29b-41d4-a716-446655440002",
        "images": [{"url": "https://example.com/barra.jpg", "alt": "Barra de Proteína"}],
        "attributes": {"proteina": "15g", "calorias": "180", "sin_gluten": true},
        "is_active": True,
        "is_featured": False,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]

@router.get("/products", response_model=ProductResponse)
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    category_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Obtener todos los productos con paginación y filtros"""
    products = MOCK_PRODUCTS.copy()
    
    # Filtrar por categoría
    if category_id:
        products = [p for p in products if p["category_id"] == category_id]
    
    # Filtrar por búsqueda
    if search:
        search_lower = search.lower()
        products = [p for p in products if search_lower in p["name"].lower() or 
                   (p["description"] and search_lower in p["description"].lower())]
    
    # Paginación
    total = len(products)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = products[start:end]
    
    return {
        "data": paginated_products,
        "total": total,
        "page": page,
        "per_page": per_page
    }

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Obtener un producto específico"""
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    """Crear un nuevo producto"""
    new_product = {
        "id": str(uuid.uuid4()),
        **product.dict(),
        "slug": product.name.lower().replace(" ", "-"),
        "short_description": product.description[:100] if product.description else None,
        "compare_price": None,
        "sku": None,
        "images": [],
        "attributes": {},
        "is_active": True,
        "is_featured": False,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
    MOCK_PRODUCTS.append(new_product)
    return new_product
