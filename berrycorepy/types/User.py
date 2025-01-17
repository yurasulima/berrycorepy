from datetime import datetime
from typing import List


from pydantic import BaseModel

from berrycorepy.types.GameProfile import GameProfile


class User(BaseModel):
    id: int
    rate: int
    telegram_id: int
    name: str
    age: int
    sex: str
    country: str
    is_deleted: bool
    is_premium: bool
    is_bot: bool
    create_at: datetime
    game_profiles: List[GameProfile]