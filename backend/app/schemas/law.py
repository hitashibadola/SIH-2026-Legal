from pydantic import AnyHttpUrl, BaseModel, Field
class LawIngestRequest(BaseModel):
    act_name:str=Field(min_length=2); section_number:str; section_title:str; statutory_text:str=Field(min_length=10); source_url:AnyHttpUrl; jurisdiction:str="India"; metadata:dict=Field(default_factory=dict)
class RetrievalRequest(BaseModel): query:str=Field(min_length=3); top_k:int=Field(5,ge=1,le=20); include_low_relevance:bool=False
class LawSearchResult(BaseModel): act_name:str; section_number:str; section_title:str; statutory_text:str; similarity:float; source_url:str
