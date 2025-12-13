from typing import List
from backend.src.core.config import settings
from backend.src.models.document import DocumentChunk
from backend.src.services.integrations import SupabaseClient, EmbeddingClient
from backend.logger.metrics import metrics

db_client = SupabaseClient(settings.SUPABASE_DB_URL, settings.VECTOR_TABLE_NAME)
embedding_client = EmbeddingClient(settings.EMBEDDING_API_KEY, settings.EMBEDDING_MODEL)

class DocumentService:
    def _chunk_text(self, text: str, chunk_size=500, overlap=50) -> List[str]:
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-overlap)]

    async def ingest_document(self, filename: str, content: bytes) -> int:
        try:
            text = content.decode('utf-8')
        except:
            return 0 

        text_chunks = self._chunk_text(text)
        docs_to_insert = []
        
        for i, chunk in enumerate(text_chunks):
            vector = embedding_client.get_embedding(chunk)
            if vector:
                docs_to_insert.append({
                    "text": chunk,
                    "source_filename": filename,
                    "chunk_id": i,
                    "embedding": str(vector) 
                })
        
        if docs_to_insert:
            db_client.upsert_documents(docs_to_insert)
        
        return len(docs_to_insert)
    @metrics.measure_time("vector_retrieval")
    async def retrieve_context(self, query: str) -> List[DocumentChunk]:
        vector = embedding_client.get_embedding(query)
        if not vector: return []
        
        results = db_client.vector_search(vector, limit=3)
        return [DocumentChunk(**res) for res in results]

document_service = DocumentService()