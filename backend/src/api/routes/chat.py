# backend/src/api/routes/chat.py
import hashlib
from fastapi import APIRouter, Depends
from backend.src.models.message import ChatRequest, ChatResponse
from backend.src.services.document_service import document_service
from backend.src.services.llm_service import llm_service
from backend.src.services.cache_service import cache_service
from backend.src.core.rate_limiter import rate_limiter

router = APIRouter()

@router.post(
    "/", 
    response_model=ChatResponse,
    dependencies=[Depends(rate_limiter)] 
)
async def chat_endpoint(request: ChatRequest):
    query = request.query.strip()
    cache_key = hashlib.sha256(query.encode()).hexdigest()

    cached = cache_service.get(cache_key)
    if cached:
        return ChatResponse(**cached)

    chunks = await document_service.retrieve_context(query)
    context_text = "\n\n".join([c.text for c in chunks])
    sources = list(set([c.source_filename for c in chunks]))

    answer = await llm_service.generate_answer(query, context_text)
    
    resp = ChatResponse(answer=answer, sources=sources)
    cache_service.set(cache_key, resp.model_dump())
    
    return resp