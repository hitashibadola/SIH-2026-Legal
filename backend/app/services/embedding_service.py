import hashlib
from app.core.exceptions import AppError
class EmbeddingService:
    def __init__(self,settings):self.settings=settings
    async def embed(self,text):
        if not self.settings.gemini_api_key:
            # Deterministic fallback is only for unconfigured local development.
            d=hashlib.sha256(text.encode()).digest();return [(d[i%32]/255)*2-1 for i in range(768)]
        try:
            from google import genai
            client=genai.Client(api_key=self.settings.gemini_api_key);response=await client.aio.models.embed_content(model=self.settings.gemini_embedding_model,contents=text);return list(response.embeddings[0].values)
        except Exception as e:raise AppError("Gemini embedding request failed",502) from e
