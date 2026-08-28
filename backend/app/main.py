from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, documents, laws, analysis, reports
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()
app = FastAPI(title="Phylax Backend", version="1.0.0", description="Indian legal document risk scanner. Not legal advice.")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(laws.router)
app.include_router(analysis.router)
app.include_router(reports.router)
