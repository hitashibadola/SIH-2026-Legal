import re
from fastapi import APIRouter, Depends
from app.api.deps import analyser, repository
from app.schemas.analysis import FullAnalysisResponse
from app.services.clause_service import detect_document_type, segment_text
router=APIRouter(prefix='/api/v1/analysis',tags=['analysis'])

def safeguards(kind,text):
    groups={'RENT_AGREEMENT':[('Notice period','notice'),('Security deposit refund timeline','deposit.*refund|refund.*deposit'),('Maintenance responsibility','maintenance|repair'),('Dispute resolution','dispute|arbitration'),('Rent escalation','escalation|increase in rent')],'EMPLOYMENT_OFFER':[('Salary/payment terms','salary|compensation'),('Notice period','notice'),('Termination procedure','termination'),('Confidentiality scope','confidential'),('Dispute resolution','dispute|arbitration')],'WEBSITE_TERMS':[('Privacy/data processing disclosures','privacy|personal data'),('Grievance mechanism','grievance'),('Refund/cancellation terms','refund|cancellation'),('Liability limitations','liability'),('Jurisdiction','jurisdiction|governing law')],'FREELANCE_CONTRACT':[('Payment terms','payment|invoice'),('Scope of work','scope|deliverable'),('Dispute resolution','dispute|arbitration')]}
    high={'Notice period','Salary/payment terms','Payment terms','Privacy/data processing disclosures'}
    return [{'safeguard':n,'status':'MISSING','importance':'HIGH' if n in high else 'MEDIUM','explanation':f'The document does not clearly address {n.lower()}. This is a completeness and negotiation concern, not an automatic legal violation.'} for n,p in groups.get(kind,[]) if not re.search(p,text,re.I)]

def summary(clauses,missing):
    # Deterministic: RED=10, YELLOW=4, GREEN=0; normalize by clauses to 0–100.
    c={x:sum(a['classification']==x for a in clauses) for x in ('RED','YELLOW','GREEN')}
    score=round(min(100,(c['RED']*10+c['YELLOW']*4)/max(1,len(clauses))*10)); level='HIGH' if score>=60 else 'MEDIUM' if score>=25 else 'LOW'
    return {'score':score,'risk_level':level,'red_flags':c['RED'],'yellow_flags':c['YELLOW'],'green_flags':c['GREEN'],'missing_safeguards':len(missing),'recommendation':'Review and negotiate before signing.' if level!='LOW' else 'No obvious high-risk issue was found; review details before signing.'}

@router.post('/{document_id}',response_model=FullAnalysisResponse)
async def analyse_document(document_id:str,repo=Depends(repository),service=Depends(analyser)):
    d=await repo.get_document(document_id);cs=await repo.clauses_for_document(document_id)
    if not cs:
        cs=segment_text(d['text_content'])
        for c in cs:c['document_id']=document_id
        cs=await repo.replace_clauses(document_id,cs)
    kind=detect_document_type(d['text_content'],d['source_type']);done=[await service.analyse_clause(c,kind) for c in cs]
    missing=safeguards(kind,d['text_content']);overall=summary(done,missing)
    result={'document_id':document_id,'document_type':kind,'overall':overall,'clauses':[{'clause_id':x.pop('id'),**x} for x in done],'missing_safeguards':missing}
    await repo.save_analysis(document_id,result);await repo.update_document(document_id,{'status':'analyzed','document_type':kind,'summary':overall})
    return result

@router.get('/{document_id}',response_model=FullAnalysisResponse)
async def get_analysis(document_id:str,repo=Depends(repository)):return await repo.get_analysis(document_id)
