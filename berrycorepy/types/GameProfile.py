from datetime import datetime

from pydantic import BaseModel


class GameProfile(BaseModel):
    id: int
    xbox: str
    create_at: datetime | None
    xuid: int | None
    uuid: str | None