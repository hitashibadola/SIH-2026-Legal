from fastapi import APIRouter, Depends, Header
from app.api.deps import repository, retrieval
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.schemas.law import LawIngestRequest, RetrievalRequest, LawSearchResult
from app.services.embedding_service import EmbeddingService
router = APIRouter(prefix='/api/v1', tags=['laws'])

@router.post('/laws/ingest')
async def ingest_law(payload:LawIngestRequest,x_admin_api_key:str|None=Header(None),repo=Depends(repository),settings=Depends(get_settings)):
    if not settings.admin_api_key or x_admin_api_key != settings.admin_api_key: raise AppError('Invalid admin API key',401)
    embedding=await EmbeddingService(settings).embed(f'{payload.act_name} Section {payload.section_number} {payload.section_title}\n{payload.statutory_text}')
    law=await repo.insert_law({**payload.model_dump(mode='json'),'source_url':str(payload.source_url),'embedding':embedding})
    return {'id':law['id'],'status':'ingested'}

@router.post('/retrieval/search')
async def search_laws(payload:RetrievalRequest,service=Depends(retrieval)):
    rows=await service.search(payload.query,payload.top_k,payload.include_low_relevance)
    return {'results':[LawSearchResult(**{k:r.get(k) for k in LawSearchResult.model_fields}).model_dump() for r in rows]}
