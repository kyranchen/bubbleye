from dataclasses import dataclass
from typing import Dict

@dataclass
class Creative:
    id: str
    name: str
    creative_type: str
    asset_id: str
    video_property: Dict[str, any]
    status: str
    createTime: str
    lastModifiedTime: str
