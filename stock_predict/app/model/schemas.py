from pydantic import BaseModel
from typing import Optional, List, Dict

class ResolveRequest(BaseModel):
    entity_name: str
    postal_code: Optional[str] = None

class ResolveResponse(BaseModel):
    input_name: str
    input_postal: Optional[str]
    matched_cmd: Optional[Dict] = None
    matched_dnb: Optional[Dict] = None
    match_confidence: float = 0.0
    graph: Optional[Dict] = None
    review_required: bool = False
