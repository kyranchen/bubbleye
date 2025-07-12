from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class CreativeGroup:
    id: str
    name: str
    creative_ids: List[str]
    status: str
    createTime: str
    lastModifiedTime: str
    performance: Dict[str, int] = field(default_factory=lambda: {"impressions": 0, "conversions": 0})
