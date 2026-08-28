"""Async PostgREST repository, with explicit in-memory local-development fallback."""
from __future__ import annotations
import json
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4
import httpx
from app.core.exceptions import AppError, NotFoundError

class Repository:
    def __init__(self, settings):
        self.settings=settings; self.remote=bool(settings.supabase_url and settings.supabase_key)
        self.memory={"documents":{},"clauses":{},"laws":{},"analyses":{}}
    def headers(self, prefer=None):
        h={"apikey":self.settings.supabase_key,"Authorization":f"Bearer {self.settings.supabase_key}","Content-Type":"application/json"}
        if prefer: h["Prefer"]=prefer
        return h
    async def request(self, method,path,params=None,payload=None,prefer=None):
        try:
            async with httpx.AsyncClient(base_url=self.settings.supabase_url.rstrip('/')+"/rest/v1",timeout=self.settings.request_timeout_seconds) as c:
                r=await c.request(method,path,params=params,json=payload,headers=self.headers(prefer))
            r.raise_for_status(); return r.json() if r.content else []
        except httpx.HTTPError as e: raise AppError("Supabase database request failed",502) from e
    async def create_document(self,data):
        data={**data,"id":str(uuid4()),"created_at":datetime.now(timezone.utc).isoformat()}
        if self.remote: return (await self.request("POST","/documents",payload=data,prefer="return=representation"))[0]
        self.memory["documents"][data["id"]]=deepcopy(data); return data
    async def get_document(self,id):
        key=str(id)
        if self.remote:
            rows=await self.request("GET","/documents",params={"id":f"eq.{key}","select":"*"})
            if not rows: raise NotFoundError("Document not found")
            return rows[0]
        if key not in self.memory["documents"]: raise NotFoundError("Document not found")
        return deepcopy(self.memory["documents"][key])
    async def update_document(self,id,changes):
        key=str(id)
        if self.remote:
            rows=await self.request("PATCH","/documents",params={"id":f"eq.{key}"},payload=changes,prefer="return=representation")
            if not rows: raise NotFoundError("Document not found")
            return rows[0]
        row=await self.get_document(key);row.update(changes);self.memory["documents"][key]=row;return row
    async def replace_clauses(self,id,clauses):
        key=str(id)
        if self.remote:
            await self.request("DELETE","/clauses",params={"document_id":f"eq.{key}"})
            return await self.request("POST","/clauses",payload=clauses,prefer="return=representation") if clauses else []
        self.memory["clauses"]={k:v for k,v in self.memory["clauses"].items() if v["document_id"]!=key}
        for x in clauses: self.memory["clauses"][x["id"]]=deepcopy(x)
        return clauses
    async def clauses_for_document(self,id):
        key=str(id)
        if self.remote:return await self.request("GET","/clauses",params={"document_id":f"eq.{key}","select":"*","order":"position.asc"})
        return sorted((deepcopy(x) for x in self.memory["clauses"].values() if x["document_id"]==key),key=lambda x:x["position"])
    async def insert_law(self,data):
        data={**data,"id":str(uuid4()),"created_at":datetime.now(timezone.utc).isoformat()}
        if self.remote:return (await self.request("POST","/law_chunks",payload=data,prefer="return=representation"))[0]
        self.memory["laws"][data["id"]]=deepcopy(data);return data
    async def law_search(self,embedding,top_k):
        if self.remote:return await self.request("POST","/rpc/match_law_chunks",payload={"query_embedding":embedding,"match_count":top_k})
        import math
        def cos(a,b): return sum(x*y for x,y in zip(a,b))/((sum(x*x for x in a)*sum(y*y for y in b))**.5 or 1)
        return sorted([{**deepcopy(x),"similarity":cos(embedding,x["embedding"])} for x in self.memory["laws"].values()],key=lambda x:x["similarity"],reverse=True)[:top_k]
    async def save_analysis(self,id,data):
        key=str(id)
        if self.remote:
            await self.request("DELETE","/document_analyses",params={"document_id":f"eq.{key}"});await self.request("POST","/document_analyses",payload={"document_id":key,"analysis":data})
        else:self.memory["analyses"][key]=deepcopy(data)
    async def get_analysis(self,id):
        key=str(id)
        if self.remote:
            rows=await self.request("GET","/document_analyses",params={"document_id":f"eq.{key}","select":"analysis"})
            if not rows:raise NotFoundError("Analysis has not been run for this document")
            return rows[0]["analysis"]
        if key not in self.memory["analyses"]:raise NotFoundError("Analysis has not been run for this document")
        return deepcopy(self.memory["analyses"][key])
