from pydantic import BaseModel

class DocumentChunk(BaseModel):
    text: str
    source_filename: str
    chunk_id: int
    class Config:
        from_attributes = True

class IngestionResult(BaseModel):
    filename: str
    chunks_ingested: int
    message: str = "Ingestion successful"