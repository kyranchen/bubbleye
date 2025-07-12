from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Campaign:
    id: str
    name: str
    status: str
    creative_group_ids: list
    type: str
    createTime: str
    lastModifiedTime: str
    impressions_goal_per_cg: Optional[int] = None
