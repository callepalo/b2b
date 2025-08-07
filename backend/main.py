from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

# Importar routers
from app.routers import productos

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
        "http://localhost:3000",  # Frontend local
        "http://localhost:8000"   # Para desarrollo local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para la respuesta de health check
class HealthCheckResponse(BaseModel):
    status: str
    version: str
    environment: str

# Incluir routers
app.include_router(productos.router)

# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Dulpromax"}

# Endpoint de health check
@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check() -> HealthCheckResponse:
    """
    Verifica el estado de la API.
    """
    return HealthCheckResponse(
        status="ok",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "production")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
