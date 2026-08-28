from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field
from .document import ClauseResponse
class LegalBasis(BaseModel): act_name:str; section_number:str; section_title:str; statutory_text:str=""; source_url:str=""; explanation:str=""; confidence:float=Field(0,ge=0,le=1)
class MissingSafeguard(BaseModel): safeguard:str; status:Literal["MISSING"]="MISSING"; importance:Literal["HIGH","MEDIUM","LOW"]; explanation:str
class ClauseAnalysisResponse(ClauseResponse):
    classification:Literal["RED","YELLOW","GREEN"]; risk_score:int=Field(ge=0,le=100); confidence:float=Field(0,ge=0,le=1); plain_english:str; reasoning:str; legal_basis:list[LegalBasis]=Field(default_factory=list); recommendation:str; negotiation_suggestion:str; missing_safeguards:list[MissingSafeguard]=Field(default_factory=list)
class OverallResponse(BaseModel): score:int; risk_level:Literal["LOW","MEDIUM","HIGH"]; red_flags:int; yellow_flags:int; green_flags:int; missing_safeguards:int; recommendation:str
class FullAnalysisResponse(BaseModel): document_id:UUID; document_type:str; overall:OverallResponse; clauses:list[ClauseAnalysisResponse]; missing_safeguards:list[MissingSafeguard]
