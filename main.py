from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from repos.socket_repository import SocketRepository
from repos.gpt_repo import GPTRepo
from models.message_request import MessageRequest

logging.basicConfig(level=logging.INFO)

app = FastAPI()
gpt_repo = GPTRepo()
socket_repo = SocketRepository()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@socket_repo.sio.on('chat')
async def chat(data: MessageRequest):
    text = data.message
    message_id = data.message_id

    async for token in gpt_repo.get_gpt_answer(text):
        await socket_repo.send_token(token, message_id)
        print(token)

    return {"status" : status.HTTP_200_OK}

@app.post('/test12')
async def test(data: MessageRequest):
    return await chat(data)


# if __name__ == "__main__":
#     kwargs = {"host": "0.0.0.0", "port": 5001}
#     kwargs.update({"reload": True})
#     uvicorn.run("main:app", **kwargs)