from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Campaign:
    ad_account_id: str
    product_id: str
    campaign_id: str
    title: str
    description: str
    status: str
    ad_group_ids: list
    type: str
    createTime: str
    lastModifiedTime: str
    impressions_goal_per_cg: Optional[int] = None

    def to_dict(self):
        return self.__dict__
