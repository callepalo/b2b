# Backend Dulpromax

API RESTful construida con FastAPI para el sistema de Dulpromax.

## Requisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

## Configuración del entorno

1. Clona el repositorio
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
ENVIRONMENT=development
APP_VERSION=1.0.0
```

## Ejecución local

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`

## Documentación

- Documentación interactiva: `/docs`
- Documentación alternativa: `/redoc`

## Endpoints

- `GET /`: Página de bienvenida
- `GET /health`: Verificación del estado de la API

## Despliegue en Render

1. Crea una nueva cuenta en [Render](https://render.com/)
2. Conecta tu repositorio de GitHub/GitLab
3. Crea un nuevo servicio Web Service
4. Selecciona el repositorio y la rama
5. Configura el servicio:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Añade las variables de entorno necesarias
7. Haz clic en "Create Web Service"

## Estructura del proyecto

```
backend/
├── main.py           # Aplicación principal
├── requirements.txt  # Dependencias
└── render.yaml       # Configuración para Render
```
