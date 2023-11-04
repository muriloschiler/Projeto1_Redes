from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    Destination_email:str
    Subject_email:str
    Body:str