import json
from app.core.exceptions import AppError
from app.prompts.legal_analysis import legal_analysis_prompt
class LegalAnalysisService:
    def __init__(self,settings,retrieval):self.settings,self.retrieval=settings,retrieval
    def insufficient(self,clause,reason="Insufficient statutory evidence retrieved."):
        return {**clause,'classification':'YELLOW','risk_score':40,'confidence':0,'plain_english':'This clause should be reviewed before acceptance.','reasoning':reason,'legal_basis':[],'recommendation':'Seek clarification or legal advice before agreeing.','negotiation_suggestion':'Ask for clearer, balanced wording.','missing_safeguards':[]}
    async def analyse_clause(self,clause,document_type):
        laws=await self.retrieval.search(clause['text'],5)
        if not laws:return self.insufficient(clause)
        if not self.settings.gemini_api_key:return self.insufficient(clause,'Gemini is not configured; no legal reasoning was generated.')
        try:
            from google import genai
            c=genai.Client(api_key=self.settings.gemini_api_key);r=await c.aio.models.generate_content(model=self.settings.gemini_model,contents=legal_analysis_prompt(clause['text'],document_type,laws),config={'response_mime_type':'application/json'});value=json.loads(r.text)
        except Exception as e:raise AppError('Gemini legal analysis request failed',502) from e
        valid={(x['act_name'],str(x['section_number'])):x for x in laws};bases=[]
        for b in value.get('legal_basis',[]):
            law=valid.get((b.get('act_name'),str(b.get('section_number'))))
            if law:bases.append({'act_name':law['act_name'],'section_number':str(law['section_number']),'section_title':law['section_title'],'statutory_text':law['statutory_text'],'source_url':law['source_url'],'explanation':str(b.get('explanation','')),'confidence':max(0,min(1,float(b.get('confidence',0))))})
        if not bases:return self.insufficient(clause) # Server-side citation grounding validation.
        klass=value.get('classification','YELLOW');klass=klass if klass in {'RED','YELLOW','GREEN'} else 'YELLOW'
        return {**clause,'classification':klass,'risk_score':max(0,min(100,int(value.get('risk_score',40)))),'confidence':max(0,min(1,float(value.get('confidence',0)))),'plain_english':str(value.get('plain_english','')),'reasoning':str(value.get('reasoning','')),'legal_basis':bases,'recommendation':str(value.get('recommendation','')),'negotiation_suggestion':str(value.get('negotiation_suggestion','')),'missing_safeguards':value.get('missing_safeguards',[])}
