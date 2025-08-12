from fastapi import APIRouter, Request, HTTPException
import os
import httpx

router = APIRouter()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
POSTGREST_URL = f"{SUPABASE_URL}/rest/v1" if SUPABASE_URL else None


def _assert_env():
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        missing = []
        if not SUPABASE_URL:
            missing.append("SUPABASE_URL")
        if not SUPABASE_ANON_KEY:
            missing.append("SUPABASE_ANON_KEY")
        raise HTTPException(status_code=500, detail=f"Backend env vars missing: {', '.join(missing)}")


@router.get("/products/prices")
async def get_products_prices(request: Request):
    """
    Devuelve productos con precio resuelto (override cliente -> segmento -> price_base).
    Proxy a la vista PostgREST `v_products_resolved` con el token del usuario para respetar RLS.
    """
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    _assert_env()

    url = f"{POSTGREST_URL}/v_products_resolved"
    headers = {
        "Authorization": auth_header,         # token del usuario
        "apikey": SUPABASE_ANON_KEY,
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=headers, params={"select": "*"})
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error contacting Supabase: {e}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()
