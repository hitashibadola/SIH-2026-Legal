class RetrievalService:
    def __init__(self,repo,embeddings,settings):self.repo,self.embeddings,self.settings=repo,embeddings,settings
    async def search(self,query,top_k,include_low_relevance=False):
        rows=await self.repo.law_search(await self.embeddings.embed(query),top_k)
        return rows if include_low_relevance else [x for x in rows if float(x.get('similarity',0))>=self.settings.retrieval_relevance_threshold]
