from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class CreativeGroup:
    id: str
    title: str
    description: str
    creative_ids: List[str]
    status: str
    createTime: str
    lastModifiedTime: str
    performance: Dict[str, int] = field(default_factory=lambda: {"impressions": 0, "conversions": 0})

    def to_dict(self):
        return self.__dict__