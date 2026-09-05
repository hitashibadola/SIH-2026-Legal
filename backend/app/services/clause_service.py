import re
from uuid import uuid4
START=re.compile(r"(?im)^(?:(ARTICLE|SECTION)\s+([A-Z0-9IVXLC]+)\s*[:.\-]?\s*(.*)|((?:\d+(?:\.\d+){0,4}|[A-Z]|[ivxlcdm]+)[.)])\s+(.+))$")
def page(text,offset):
    found=[int(x.group(1)) for x in re.finditer(r"\[Page (\d+)\]",text) if x.start()<=offset]
    return found[-1] if found else None
def segment_text(text):
    matches=list(START.finditer(text))
    if not matches:matches=list(re.finditer(r"(?m)^.+(?:\n.+){0,8}(?=\n\n|\Z)",text))
    out=[]
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(text);body=text[m.start():end].strip()
        if len(body)<30:continue
        g=m.groups() if m.re is START else ();number=(g[1] or g[3].rstrip(').')) if g else None;heading=(g[2] or g[4]) if g else None
        out.append({'id':str(uuid4()),'position':len(out),'clause_number':number,'title':heading[:160] if heading and len(heading)<160 else None,'text':body,'page_start':page(text,m.start()),'page_end':page(text,end)})
    return out or [{'id':str(uuid4()),'position':0,'clause_number':None,'title':None,'text':text,'page_start':1,'page_end':None}]
def detect_document_type(text,source_type):
    low=text.lower();signals={'RENT_AGREEMENT':['landlord','tenant','security deposit','premises','monthly rent'],'EMPLOYMENT_OFFER':['employer','employee','salary','notice period','joining date'],'FREELANCE_CONTRACT':['independent contractor','freelance','statement of work','invoice'],'WEBSITE_TERMS':['terms of service','terms and conditions','our website','user account']}
    if source_type=='url':signals['WEBSITE_TERMS'].append('privacy')
    points={k:sum(x in low for x in v) for k,v in signals.items()};best=max(points,key=points.get)
    return best if points[best]>=2 else 'UNKNOWN'
