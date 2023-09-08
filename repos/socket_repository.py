from typing import Any
import socketio

sio: Any = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)

class SocketRepository:
    def __init__(self):
        self.sio = sio
        self.socket_app = socket_app

    async def send_token(self, token: str, message_id: str):
        await self.sio.emit('new_token', {'message_id': message_id, 'token': token})
    
    # TODO(arcthurus): Нужно ли полное сообщение тут отправлять?
    async def send_message_end(self, message_id: str, text: str):
        await self.sio.emit('message_end', {'ended_message_id': message_id})