from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_supabase(use_service_role: bool = True) -> Client:
    """
    Crea y retorna un cliente de Supabase configurado
    
    Args:
        use_service_role (bool): Si es True, usa la clave de servicio (para operaciones del lado del servidor).
                              Si es False, usa la clave anónima (para operaciones del lado del cliente).
    """
    supabase_url = os.getenv("SUPABASE_URL")
    
    if use_service_role:
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE")
        if not supabase_key:
            raise ValueError("SUPABASE_SERVICE_ROLE debe estar configurado en las variables de entorno")
    else:
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        if not supabase_key:
            raise ValueError("SUPABASE_ANON_KEY debe estar configurado en las variables de entorno")
    
    if not supabase_url:
        raise ValueError("SUPABASE_URL debe estar configurado en las variables de entorno")
    
    return create_client(supabase_url, supabase_key)
