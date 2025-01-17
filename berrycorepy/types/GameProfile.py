from datetime import datetime
from typing import Optional
from berrycorepy.types.base import DangerousObject


class GameProfile(DangerousObject):
    id: Optional[int]
    xbox: Optional[str]
    xuid: Optional[int]
    uuid: Optional[str]
    create_at: datetime