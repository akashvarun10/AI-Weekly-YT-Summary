from pydantic import BaseModel
from typing import List

class User(BaseModel):
    email: str
    channels: List[str]