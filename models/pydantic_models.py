from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    id: str
    telegram_id: str
    name: str
    email: str
    tokens_used: str
    created_at: datetime

class MessageBase(BaseModel):
    id: str
    text: str
    user_id: str
    source: str
    related_message_id: str
    created_at: datetime
    channel_id: str
