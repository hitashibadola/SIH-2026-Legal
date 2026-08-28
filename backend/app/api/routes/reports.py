from fastapi import APIRouter, Depends
from fastapi.responses import Response
from app.api.deps import repository
from app.services.report_service import build_report
router=APIRouter(prefix='/api/v1/reports',tags=['reports'])
@router.get('/{document_id}/pdf')
async def pdf_report(document_id:str,repo=Depends(repository)):
    document,analysis=await repo.get_document(document_id),await repo.get_analysis(document_id)
    return Response(build_report(document,analysis),media_type='application/pdf',headers={'Content-Disposition':f'attachment; filename="phylax-{document_id}.pdf"'})
