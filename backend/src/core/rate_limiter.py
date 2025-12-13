import time
from fastapi import Request, HTTPException
request_history = {}

RATE_LIMIT_COUNT = 10
RATE_LIMIT_WINDOW = 60 

async def rate_limiter(request: Request):
    """
    Blocks an IP if they send too many requests too quickly.
    """
    client_ip = request.client.host
    now = time.time()

    if client_ip not in request_history:
        request_history[client_ip] = []

    history = request_history[client_ip]
    valid_requests = [t for t in history if now - t < RATE_LIMIT_WINDOW]
    request_history[client_ip] = valid_requests

    if len(valid_requests) >= RATE_LIMIT_COUNT:
        raise HTTPException(
            status_code=429, 
            detail="Rate limit exceeded. Please try again in a minute."
        )

    request_history[client_ip].append(now)