from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile
from app.api.deps import repository
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.schemas.document import DocumentExtractionResponse, DocumentResponse, URLExtractionRequest
from app.services.pdf_service import extract_pdf
from app.services.web_scraper import extract_terms
from app.services.clause_service import segment_text
router = APIRouter(prefix='/api/v1/documents', tags=['documents'])

@router.post('/upload', response_model=DocumentExtractionResponse)
async def upload_document(file:UploadFile=File(...), repo=Depends(repository), settings=Depends(get_settings)):
    if Path(file.filename or '').suffix.lower() != '.pdf' or file.content_type not in {'application/pdf','application/x-pdf'}: raise AppError('Only PDF files are accepted',415)
    content=await file.read()
    if len(content)>settings.max_file_size_mb*1024*1024: raise AppError('PDF exceeds configured size limit',413)
    if not content.startswith(b'%PDF'): raise AppError('Uploaded file is not a valid PDF',415)
    text,pages=await extract_pdf(content)
    doc=await repo.create_document({'source_type':'pdf','filename':Path(file.filename).name,'text_content':text,'page_count':len(pages),'character_count':len(text),'status':'extracted','metadata':{'pages':pages}})
    return {'document_id':doc['id'],'source_type':'pdf','filename':doc['filename'],'page_count':len(pages),'character_count':len(text),'status':'extracted'}

@router.post('/url', response_model=DocumentExtractionResponse)
async def extract_url(payload:URLExtractionRequest, repo=Depends(repository), settings=Depends(get_settings)):
    text,url=await extract_terms(str(payload.url),settings)
    doc=await repo.create_document({'source_type':'url','source_url':url,'text_content':text,'character_count':len(text),'status':'extracted'})
    return {'document_id':doc['id'],'source_type':'url','url':url,'character_count':len(text),'status':'extracted'}

@router.get('/{document_id}', response_model=DocumentResponse)
async def get_document(document_id:str, repo=Depends(repository)):
    d=await repo.get_document(document_id); cs=await repo.clauses_for_document(document_id)
    return {'document_id':d['id'],'source_type':d['source_type'],'filename':d.get('filename'),'url':d.get('source_url'),'status':d['status'],'created_at':d['created_at'],'summary':d.get('summary',{}),'clauses':[{'clause_id':c['id'],**{k:c.get(k) for k in ('clause_number','title','text','page_start','page_end')}} for c in cs]}

@router.post('/{document_id}/segment')
async def segment_document(document_id:str, repo=Depends(repository)):
    d=await repo.get_document(document_id); cs=segment_text(d['text_content'])
    for c in cs: c['document_id']=document_id
    cs=await repo.replace_clauses(document_id,cs); await repo.update_document(document_id,{'status':'segmented'})
    return {'document_id':document_id,'status':'segmented','clauses':[{'clause_id':c['id'],**{k:c.get(k) for k in ('clause_number','title','text','page_start','page_end')}} for c in cs]}
