from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_supabase() -> Client:
    """
    Crea y retorna un cliente de Supabase configurado
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL y SUPABASE_SERVICE_ROLE deben estar configurados en las variables de entorno")
    
    return create_client(supabase_url, supabase_key)
