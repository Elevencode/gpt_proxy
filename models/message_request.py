from pydantic import BaseModel

class MessageRequest(BaseModel):
    message_id: str
    message: str