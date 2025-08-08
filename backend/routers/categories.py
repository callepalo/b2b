from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import uuid

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

# Datos de ejemplo
MOCK_CATEGORIES = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Proteínas",
        "description": "Suplementos proteicos en polvo y listos para consumir",
        "slug": "proteinas",
        "parent_id": None,
        "image_url": None,
        "is_active": True,
        "sort_order": 1,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "name": "Snacks Saludables",
        "description": "Snacks bajos en azúcar y ricos en nutrientes",
        "slug": "snacks-saludables",
        "parent_id": None,
        "image_url": None,
        "is_active": True,
        "sort_order": 2,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]

@router.get("/categories", response_model=CategoryResponse)
async def get_categories():
    """Obtener todas las categorías"""
    return {
        "data": MOCK_CATEGORIES,
        "total": len(MOCK_CATEGORIES)
    }

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    """Obtener una categoría específica"""
    category = next((c for c in MOCK_CATEGORIES if c["id"] == category_id), None)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@router.post("/categories", response_model=Category)
async def create_category(category: CategoryCreate):
    """Crear una nueva categoría"""
    new_category = {
        "id": str(uuid.uuid4()),
        **category.dict(),
        "image_url": None,
        "is_active": True,
        "sort_order": 0,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
    MOCK_CATEGORIES.append(new_category)
    return new_category
