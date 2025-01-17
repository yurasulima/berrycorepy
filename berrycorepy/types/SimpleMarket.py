from datetime import datetime

from pydantic import BaseModel

from berrycorepy.types.User import User


class SimpleMarket(BaseModel):
    id: int
    content: str
    user: User
    createAt: datetime