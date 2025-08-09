import os
from functools import lru_cache
from supabase import create_client, Client

SUPABASE_URL_ENV = "SUPABASE_URL"
SUPABASE_SERVICE_ROLE_ENV = "SUPABASE_SERVICE_ROLE"

@lru_cache(maxsize=1)
def get_supabase() -> Client:
    url = os.getenv(SUPABASE_URL_ENV)
    key = os.getenv(SUPABASE_SERVICE_ROLE_ENV)
    if not url or not key:
        missing = []
        if not url:
            missing.append(SUPABASE_URL_ENV)
        if not key:
            missing.append(SUPABASE_SERVICE_ROLE_ENV)
        raise RuntimeError(f"Supabase env vars missing: {', '.join(missing)}")
    return create_client(url, key)
