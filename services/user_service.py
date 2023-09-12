import logging
from fastapi import status
from typing import Dict, Union

from repos.db_repo import DBRepo
from models.schemas import User

logging.basicConfig(level=logging.INFO)

class UserService:
    def __init__(self, repo: DBRepo):
        self.repo = repo

    async def create_user(self, user: User) -> Dict[str, Union[str, int]]:
        try:
            created_user_id = await self.repo.create_user(user)
            return created_user_id
        except Exception as e:
            logging.exception('Error creating user')
            return {'Message': 'Create user error', "status" : type(e).__name__}
        

    async def update_user(self, user: User) -> Dict[str, Union[str, int]]:
        try:
            updated_user_id = await self.repo.update_user(user)
            return updated_user_id
        except Exception as e:
            logging.exception('Error updating user')
            return {'Message': 'Update user error', "status" : type(e).__name__}