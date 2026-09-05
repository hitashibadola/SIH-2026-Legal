from functools import lru_cache
from app.core.config import get_settings
from app.db.supabase import Repository
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.legal_analysis_service import LegalAnalysisService

@lru_cache
def repository(): return Repository(get_settings())
@lru_cache
def retrieval(): return RetrievalService(repository(), EmbeddingService(get_settings()), get_settings())
@lru_cache
def analyser(): return LegalAnalysisService(get_settings(), retrieval())
