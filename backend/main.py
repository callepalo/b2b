from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Dict, Any

app = FastAPI(
    title="Dulpromax API",
    description="API para el sistema de Dulpromax",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplazar con los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Si necesitas agregar más endpoints, puedes hacerlo aquí

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
