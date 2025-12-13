from backend.src.core.config import settings
from backend.src.services.integrations import LLMClient
from backend.logger.metrics import metrics

llm_client = LLMClient(settings.LLM_API_KEY, settings.LLM_MODEL)

SYSTEM_PROMPT = """
You are a helpful AI Assistant. Answer the user question based ONLY on the provided context below.
If the answer is not in the context, say "I don't have that information."
"""

class LLMService:
    @metrics.measure_time("llm_generation")
    async def generate_answer(self, query: str, context: str) -> str:
        if not context:
            return "I couldn't find any relevant documents to answer your question."
            
        full_prompt = f"""
        {SYSTEM_PROMPT}
        
        --- CONTEXT ---
        {context}
        --- END CONTEXT ---
        
        USER QUESTION: {query}
        """
        
        return llm_client.get_completion(full_prompt)

llm_service = LLMService()