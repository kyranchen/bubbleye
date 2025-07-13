from dataclasses import dataclass
from typing import Dict

@dataclass
class Creative:
    id: str
    ad_account_id: str
    product_id: str
    title: str
    type: str
    video_property: Dict[str, any]
    createTime: str
    lastModifiedTime: str
