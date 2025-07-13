from dataclasses import dataclass, field
from typing import Dict

@dataclass
class AdGroup:
    ad_group_id: str
    campaign_id: str
    creative_group_ids: list
    performance: Dict[str, int] = field(default_factory=lambda: {"impressions": 0, "conversions": 0})

    def to_dict(self):
        return self.__dict__
