from fastapi import Header, HTTPException, Security
from .config import settings

async def verify_admin_key(x_api_key: str = Header(...)):
    """
    Protects Admin routes (like Upload). 
    Requires 'x-api-key' header to match the .env ADMIN_API_KEY.
    """
    if x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=403, 
            detail="Invalid or missing Admin API Key."
        )
    return x_api_key