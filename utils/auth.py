from fastapi import Request, HTTPException
from dotenv import load_dotenv
import logging
import os
import ast


load_dotenv()
logging.basicConfig(level=logging.INFO)

keys = ast.literal_eval(os.getenv("API_KEYS"))

def verify_secret_key(request: Request):
    key = request.headers.get("Authorization")
    if key not in keys:
        raise HTTPException(status_code=401, detail="Invalid api key")
    return key

def verify_socket_connection(environ) -> bool:
    key = environ.get('HTTP_AUTHORIZATION')
    print(key)
    if not key or key not in keys:
        return False
    return True