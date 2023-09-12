from models.schemas import User, Message
from models.pydantic_models import UserBase, MessageBase

def user_pydantic_to_sqlalchemy(pydantic_model: UserBase) -> User:
    return User(
        id=pydantic_model.id,
        telegram_id=pydantic_model.telegram_id,
        name=pydantic_model.name,
        email=pydantic_model.email,
        tokens_used=pydantic_model.tokens_used,
        created_at=pydantic_model.created_at
    )

def message_pydantic_to_sqlalchemy(pydantic_model: MessageBase) -> Message:
    return Message(
        id=pydantic_model.id,
        text=pydantic_model.text,
        user_id=pydantic_model.user_id,
        source=pydantic_model.source,
        related_message_id=pydantic_model.related_message_id,
        created_at=pydantic_model.created_at,
        channel_id=pydantic_model.channel_id
    )
