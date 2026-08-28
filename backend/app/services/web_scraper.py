import ipaddress,re,socket
from urllib.parse import urljoin,urlparse
import httpx
from bs4 import BeautifulSoup
from app.core.exceptions import AppError
from .pdf_service import normalize_text
def validate_public_url(url):
    p=urlparse(url);host=(p.hostname or '').rstrip('.').lower()
    if p.scheme not in {'http','https'} or not host or p.username or p.password:raise AppError("Only public http(s) URLs are allowed")
    if host in {'localhost','localhost.localdomain'} or host.endswith('.local'):raise AppError("Internal URLs are not allowed")
    try: addresses={x[4][0] for x in socket.getaddrinfo(host,None)}
    except socket.gaierror as e:raise AppError("URL host could not be resolved") from e
    if any(not ipaddress.ip_address(a).is_global for a in addresses):raise AppError("Internal network addresses are not allowed")
async def extract_terms(url,settings):
    if len(url)>settings.max_url_length:raise AppError("URL exceeds configured maximum length")
    validate_public_url(url)
    try:
        # Check each hop before it is requested so a public URL cannot redirect us into a private network.
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds,follow_redirects=False,headers={'User-Agent':'Phylax/1.0'}) as c:
            current=url
            for _ in range(5):
                validate_public_url(current); r=await c.get(current)
                if r.status_code not in {301,302,303,307,308}: break
                location=r.headers.get('location')
                if not location: raise AppError('Redirect response did not include a location',422)
                current=urljoin(current,location)
            else: raise AppError('Too many redirects',422)
        r.raise_for_status()
    except httpx.HTTPError as e:raise AppError("Could not fetch requested URL",422) from e
    validate_public_url(str(r.url))
    if 'html' not in r.headers.get('content-type','').lower():raise AppError("URL must return HTML",422)
    soup=BeautifulSoup(r.text,'html.parser')
    for tag in soup(['script','style','noscript','nav','footer','aside','form','iframe']):tag.decompose()
    for tag in soup.find_all(attrs={'class':re.compile('cookie|banner|advert|promo|newsletter',re.I)}):tag.decompose()
    choices=soup.select("main,article,[id*='terms' i],[class*='terms' i],[id*='privacy' i],[class*='privacy' i],[role='main']")
    root=max(choices,key=lambda x:len(x.get_text(' ',strip=True)),default=soup.body or soup);text=normalize_text(root.get_text('\n',strip=True))
    if len(text)<settings.min_web_text_characters:raise AppError("Page did not contain enough meaningful terms text",422)
    return text,str(r.url)
