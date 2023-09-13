from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    id: str
    telegram_id: Optional[str]
    name: str
    email: str
    tokens_used: str
    created_at: datetime

class MessageBase(BaseModel):
    id: str
    text: str
    user_id: str
    source: str
    related_message_id: Optional[str]
    created_at: datetime
    channel_id: str
