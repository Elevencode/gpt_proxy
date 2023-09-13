import socketio
import uuid
from datetime import datetime
from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

app = FastAPI()

socket_key = os.getenv('TEST_KEY')

sio = socketio.AsyncClient()
endpoint = 'http://127.0.0.1:8000'

@sio.on('new_token')
async def on_new_token(data):
    logging.info(data)

@sio.on('message_end')
async def on_message_end(data):
    logging.info(data)

@sio.on("connect")
async def connect():
    logging.info("connected")
    
    request = {
    'id': str(uuid.uuid4()),
    'text': 'Hello!',
    'user_id': 'test_id',
    'source': 'chat',
    'related_message_id': str(uuid.uuid4()),
    'created_at': datetime.now().isoformat(),
    'channel_id': str(uuid.uuid4()),
}

    await sio.emit('chat', request)
    logging.info('Message sent!')


@app.on_event("startup")
async def start_app():
    try:
        await sio.connect(endpoint, {'Authorization': socket_key})
        await sio.wait()
    except Exception as e:
        logging.exception(f"Startup exception: {str(e)}")


if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 8000}
    kwargs.update({"reload": True})
    uvicorn.run("client:app", **kwargs)