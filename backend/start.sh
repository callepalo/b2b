#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar la aplicación
uvicorn main:app --host 0.0.0.0 --port $PORT
