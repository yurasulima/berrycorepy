from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from berrycorepy.types.GameProfile import GameProfile
from berrycorepy.types.base import DangerousObject


class User(DangerousObject):
    id: Optional[int]
    rate: Optional[int]
    telegram_id: Optional[int]
    name: Optional[str]
    age: Optional[int]
    sex: Optional[str]
    country: Optional[str]
    is_deleted: Optional[bool]
    is_premium: Optional[bool]
    is_bot: Optional[bool]
    create_at: datetime
    game_profiles: List[GameProfile]