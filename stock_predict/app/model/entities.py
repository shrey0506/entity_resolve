from pydantic import BaseModel
from typing import List, Optional, Dict

class Entity(BaseModel):
    entity_id: str
    canonical_name: str
    duns: Optional[str] = None
    postal_codes: List[str] = []
    sources: List[Dict] = []
    confidence: float = 1.0

class Relationship(BaseModel):
    from_entity: str
    to_entity: str
    rel_type: str   # HAS_SUBSIDIARY | PARENT_OF | UBO_OF
    pct: Optional[float] = None
    confidence: float = 1.0
