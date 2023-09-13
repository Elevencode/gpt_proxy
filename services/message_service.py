from repos.db_repo import DBRepo
from repos.socket_repository import SocketRepository
from repos.gpt_repo import GPTRepo
from models.schemas import Message
from utils.converters import messages_to_gpt_messages
import logging
import random

logging.basicConfig(level=logging.INFO)

class MessageService:
    def __init__(self, gpt_repo: GPTRepo, socket_repo: SocketRepository, db_repo: DBRepo):
        self.gpt_repo = gpt_repo
        self.socket_repo = socket_repo
        self.db_repo = db_repo

    async def handle_message(self, message: Message):
        context = await self.db_repo.get_messages(message.channel_id, 5)
        gpt_context = messages_to_gpt_messages(context)
        print(message.related_message_id)
        answer_message = Message(
            id=message.related_message_id,
            text='',
            user_id=message.user_id,
            source='AI',
            channel_id=message.channel_id,
            related_message_id=message.id
        )

        try:
            if not await self.db_repo.channel_exists(message.channel_id):
                await self.db_repo.create_channel(message.channel_id)
                
            await self.db_repo.create_message(message)
            async for token in self.gpt_repo.get_gpt_answer(message.text, gpt_context):
                await self.socket_repo.send_token(token, message.related_message_id)
                answer_message.text += token
                print(token)
            await self.db_repo.create_message(answer_message)
            await self.socket_repo.send_message_end(answer_message.id)
        except Exception as e:
            logging.exception('Error creating message')
            await self.socket_repo.send_gpt_request_error(answer_message.id, str(e))
            return {'Message': 'Create message error', "status" : type(e).__name__}
        
    async def mock_handle_message(self, message: Message):
        context = await self.db_repo.get_messages(message.channel_id, 5)
        answer_message = Message(
            id=message.related_message_id,
            text='',
            user_id=message.user_id,
            source='AI',
            channel_id=message.channel_id,
            related_message_id=message.id
        )

        await self.db_repo.create_message(message)

        words = ["hello", "world", "this", "is", "a", "mock", "message", "from", "GPTRepo"]
        response = " ".join(random.choices(words, k=20))
        
        tokens = response.split()
        for token in tokens:
            await self.socket_repo.send_token(token, message.id)
            answer_message.text += token
            print(token)

        await self.db_repo.create_message(answer_message)
        await self.socket_repo.send_message_end(message.id)