from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
def build_report(document,analysis):
    out=BytesIO();s=getSampleStyleSheet();story=[Paragraph('PHYLAX',s['Title']),Paragraph('Indian Legal Document Risk Report',s['Heading2']),Spacer(1,12)];o=analysis['overall']
    story += [Paragraph(f"Document: {document.get('filename') or document.get('source_url') or document['id']}",s['BodyText']),Paragraph(f"Document type: {analysis['document_type']}",s['BodyText']),Paragraph(f"Overall risk score: <b>{o['score']}/100 ({o['risk_level']})</b>",s['Heading3']),Paragraph(o['recommendation'],s['BodyText']),Spacer(1,10)]
    table=Table([['Classification','Count'],['Red flags',o['red_flags']],['Yellow flags',o['yellow_flags']],['Green flags',o['green_flags']],['Missing safeguards',o['missing_safeguards']]],colWidths=[250,120]);table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#163c5b')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.5,colors.grey),('PADDING',(0,0),(-1,-1),6)]));story += [table,Spacer(1,10),Paragraph('Clause analysis',s['Heading2'])]
    for c in analysis['clauses']:story += [Paragraph(f"{c.get('clause_number') or 'Clause'} — {c.get('title') or c['classification']}",s['Heading3']),Paragraph(f"<b>{c['classification']}</b>: {c['plain_english']}",s['BodyText']),Paragraph(c['reasoning'],s['BodyText']),Spacer(1,6)]
    SimpleDocTemplate(out,pagesize=A4,title='Phylax Legal Risk Report').build(story);return out.getvalue()
