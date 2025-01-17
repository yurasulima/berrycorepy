from pydantic import BaseModel


class UserTime(BaseModel):
    xbox: str
    time: str