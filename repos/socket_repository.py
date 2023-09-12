from typing import Any
import socketio

sio: Any = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)

class SocketRepository:
    def __init__(self):
        self.sio = sio
        self.socket_app = socket_app

    async def send_token(self, token: str, message_id: str):
        """
        Sends a token of an OpenAI answer to client through SocketIO .

        Params:
        - token (str): chunk on GPT answer.
        - message_id (str): id of answer (temporary) message

        Returns:
        - None
        """
        await self.sio.emit('new_token', {'message_id': message_id, 'token': token})
    
    # TODO(arcthurus): Нужно ли полное сообщение тут отправлять?
    async def send_message_end(self, message_id: str):
        """
        Sends the message id for which token generation has been completed

        Params:
        - message_id (str): id of answer (temporary) message

        Returns:
        - None
        """
        await self.sio.emit('message_end', {'ended_message_id': message_id})
    
    async def send_gpt_request_error(self, message_id: str, error_text: str):
        """
        Sends the error text and message id in case of OpenAI error.

        Params:
        - message_id (str): id of answer (temporary) message
        - error_text (str): error message

        Returns:
        - None
        """
        await self.sio.emit('gpt_error', {'message_id': message_id, 'error': error_text})

    async def send_socket_error(self, data):
        await self.sio.emit('error', data)