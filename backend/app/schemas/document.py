from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
class URLExtractionRequest(BaseModel): url: HttpUrl
class DocumentExtractionResponse(BaseModel):
    document_id: UUID; source_type: str; filename: str|None=None; url: str|None=None; page_count: int|None=None; character_count:int; status:str
class ClauseResponse(BaseModel):
    clause_id: UUID; clause_number:str|None=None; title:str|None=None; text:str; page_start:int|None=None; page_end:int|None=None
class DocumentResponse(BaseModel):
    document_id:UUID; source_type:str; filename:str|None=None; url:str|None=None; status:str; created_at:datetime; summary:dict=Field(default_factory=dict); clauses:list[ClauseResponse]=Field(default_factory=list)
