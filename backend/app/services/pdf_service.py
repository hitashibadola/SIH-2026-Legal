import asyncio,io,re,pdfplumber
from app.core.exceptions import AppError
def normalize_text(text): return re.sub(r"[ \t]+"," ",re.sub(r"\n{3,}","\n\n",text.replace("\r","\n"))).strip()
def extract(content):
    try:
        pages=[]
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for n,page in enumerate(pdf.pages,1):pages.append({"page":n,"text":normalize_text(page.extract_text() or "")})
    except Exception as e:raise AppError("The uploaded file could not be read as a PDF") from e
    text=normalize_text("\n\n".join(f"[Page {p['page']}]\n{p['text']}" for p in pages if p['text']))
    if not text:raise AppError("No selectable text was found. This appears to be a scanned/image-only PDF; OCR is required.",422)
    return text,pages
async def extract_pdf(content):return await asyncio.to_thread(extract,content)
