import google.generativeai as genai
from groq import Groq
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List

class SupabaseClient:
    def __init__(self, db_url: str, vector_table: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.vector_table = vector_table

    def upsert_documents(self, documents: List[dict]):
        with self.engine.connect() as conn:
            for doc in documents:
                stmt = text(f"""
                    INSERT INTO {self.vector_table} (text, source_filename, chunk_id, embedding)
                    VALUES (:text, :source_filename, :chunk_id, :embedding)
                """)
                conn.execute(stmt, doc)
            conn.commit()

    def vector_search(self, query_embedding: List[float], limit: int) -> List[dict]:
        with self.engine.connect() as conn:
            stmt = text(f"""
                SELECT text, source_filename, chunk_id 
                FROM {self.vector_table}
                ORDER BY embedding <=> :embedding
                LIMIT :limit
            """)
            result = conn.execute(stmt, {"embedding": str(query_embedding), "limit": limit})
            return [dict(row._mapping) for row in result]

class EmbeddingClient:
    def __init__(self, api_key: str, model_name: str):
        genai.configure(api_key=api_key)
        self.model = model_name

    def get_embedding(self, text: str) -> List[float]:
        if not text: return []
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Gemini Embedding Error: {e}")
            return []

class LLMClient:
    def __init__(self, api_key: str, model_name: str):
        self.client = Groq(api_key=api_key)
        self.model = model_name

    def get_completion(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.0
        )
        return completion.choices[0].message.content