from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.routes import documents, chat
from backend.src.core.config import settings
from backend.logger.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="GenAI Backend with RAG"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/docs", tags=["Admin"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["Chat"])

@app.get("/")
async def root():
    logger.info("Health check accessed.")
    return {"status": "active", "app": settings.PROJECT_NAME}

@app.on_event("startup")
async def startup_event():
    logger.info("Server starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Server shutting down...")