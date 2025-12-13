import os
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".txt", ".md", ".csv", ".json"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024 # 5MB

async def validate_file(file: UploadFile):
    filename = file.filename if file.filename else ""
    _, ext = os.path.splitext(filename)
    
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type '{ext}' not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )

    if file.headers.get("content-length"):
        file_size = int(file.headers.get("content-length"))
        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="File too large (Max 5MB).")
            
    return True