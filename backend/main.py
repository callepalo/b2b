from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ping, categories, products

app = FastAPI(
    title="DulcePromax API",
    description="API para catálogo de productos saludables B2B",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dulpromax.netlify.app",
        "http://localhost:5173",  # Para desarrollo local
        "http://localhost:3000",  # Puerto alternativo
    ],
    # Permite también cualquier subdominio de Netlify (deploy previews)
    allow_origin_regex=r"^https://([a-z0-9-]+)\.netlify\.app$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(ping.router, prefix="/api/v1", tags=["health"])
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
