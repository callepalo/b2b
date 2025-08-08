from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong", "status": "ok"}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dulcepromax-api"}
