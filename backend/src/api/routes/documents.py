from fastapi import APIRouter, UploadFile, File, Depends
from backend.src.services.document_service import document_service
from backend.src.models.document import IngestionResult
from backend.src.utils.validators import validate_file
from backend.src.core.security import verify_admin_key

router = APIRouter()

@router.post(
    "/upload", 
    response_model=IngestionResult,
    dependencies=[Depends(verify_admin_key)] # <-- THIS LOCKS THE ROUTE
)
async def upload_document(file: UploadFile = File(...)):
    await validate_file(file)
    content = await file.read()
    count = await document_service.ingest_document(file.filename, content)
    
    return IngestionResult(filename=file.filename, chunks_ingested=count)