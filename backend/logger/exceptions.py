# backend/data/logger/exceptions.py

class DocumentIngestionError(Exception):
    """Custom exception raised for errors during document parsing, chunking, or vector storage."""
    def __init__(self, message="Document ingestion failed", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class LLMServiceError(Exception):
    """Custom exception raised for errors during communication with the LLM API (Groq/OpenAI)."""
    def __init__(self, message="LLM API call failed", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class CacheServiceError(Exception):
    """Custom exception raised for errors during interaction with the caching layer (Redis)."""
    def __init__(self, message="Caching operation failed", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class DatabaseConnectionError(Exception):
    """Custom exception for issues connecting to Supabase/Postgres."""
    def __init__(self, message="Database connection or query failed", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)