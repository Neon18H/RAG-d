from pydantic import BaseModel
from typing import List, Optional

class Doc(BaseModel):
    id: str
    text: str
    meta: Optional[dict] = None

class UpsertRequest(BaseModel):
    docs: List[Doc]

class SearchRequest(BaseModel):
    query: str
    top_k: int = 4
