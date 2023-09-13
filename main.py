from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from services.user_service import UserService
from services.message_service import MessageService
from repos.socket_repository import SocketRepository
from repos.gpt_repo import GPTRepo
from repos.db_repo import DBRepo
from models.schemas import Message, User
from models.pydantic_models import MessageBase, UserBase
from utils.converters import user_pydantic_to_sqlalchemy, message_pydantic_to_sqlalchemy
from utils.auth import verify_secret_key, verify_socket_connection
from utils.info import description

logging.basicConfig(level=logging.INFO)

app = FastAPI(title='gpt_proxy', version='1.0.0', description=description)

gpt_repo = GPTRepo()
socket_repo = SocketRepository()
db_repo = DBRepo()
user_service = UserService(repo=db_repo)
message_service = MessageService(gpt_repo, socket_repo, db_repo)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", socket_repo.socket_app)

@app.on_event("startup")
async def startup_event():
    try:
        await db_repo.connect()
        logging.info('connected to DB')
    except Exception as e:
        logging.error('error connection')

@socket_repo.sio.on('chat')
async def chat(sid, data):
    message = message_pydantic_to_sqlalchemy(MessageBase(**data))
    await message_service.handle_message(message)
    # await message_service.mock_handle_message(message)

@socket_repo.sio.event
async def connect(sid, environ):
    auth_result = verify_socket_connection(environ)
    if auth_result == True:
        return True
    else:
        socket_repo.send_socket_error({'detail': 'Invalid token'})
        return False

@app.post('/user', tags=['User'], summary="Creates a new user", description="This endpoint requires an api_key to be sent in the Authorization Header")
async def create_user(data: UserBase, key: str = Depends(verify_secret_key)):
    user = user_pydantic_to_sqlalchemy(data)
    await user_service.create_user(user)

@app.put('/user', tags=['User'], summary="Updates a user", description="This endpoint requires an api_key to be sent in the Authorization Header")
async def update_user(data: UserBase, key: str = Depends(verify_secret_key)):
    user = user_pydantic_to_sqlalchemy(data)
    await user_service.update_user(user)




# if __name__ == "__main__":
#     kwargs = {"host": "0.0.0.0", "port": 5001}
#     kwargs.update({"reload": True})
#     uvicorn.run("main:app", **kwargs)