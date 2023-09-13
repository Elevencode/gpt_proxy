import asyncpg
import os
import logging
from dotenv import load_dotenv
from typing import List

from models.schemas import User, Message
from utils.converters import db_record_to_message

load_dotenv()
logging.basicConfig(level=logging.INFO)

class DBRepo:
    db = os.getenv('DATABASE_NAME')
    db_user = os.getenv('DATABASE_USER')
    db_password = os.getenv('DATABASE_PASSWORD')
    db_host = os.getenv('DATABASE_HOST')

    async def connect(self):
        """
        Establishes a connection pool to the database.

        This method initializes a connection pool to the database using the class's database configurations. 
        The pool can then be used to acquire individual connections for executing database operations.

        Usage:
        >>> await db_repo.connect()
        """

        self.pool = await asyncpg.create_pool(database=self.db, user=self.db_user, password=self.db_password, host=self.db_host)

    async def create_user(self, user: User):
        """
        Inserts a new user into the database.

        Parameters:
        - user (User): The user object containing the user's details.

        Returns:
        - str: The ID of the created user.

        Usage:
        >>> user = User(id="123", telegram_id="456", name="John", email="johndoe@example.com", tokens_used="10", created_at=datetime.now())
        >>> created_user_id = await db_repo.create_user(user)
        >>> print(created_user_id)
        123
        """

        async with self.pool.acquire() as conn:
            INSERT_SQL = """
            INSERT INTO Users (id, telegram_id, name, email, tokens_used, created_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            """
            return await conn.fetchval(INSERT_SQL, user.id, user.telegram_id, user.name, user.email, user.tokens_used, user.created_at)

    async def update_user(self, user: User):
        """
        Updates user in DB.

        Params:
        - user (User): Object with updated info.

        Returns:
        - str: Updated user id. Returns None if user not found.

        Usage:
        >>> user = User(id="123", telegram_id="456", name="John", email="johndoe@example.com", tokens_used="10", created_at=datetime.now())
        >>> updated_user_id = await db_repo.update_user(user)
        >>> print(updated_user_id)
        123
        """
        async with self.pool.acquire() as conn:
            UPDATE_SQL = """
            UPDATE Users
            SET telegram_id = $2, name = $3, email = $4, tokens_used = $5, created_at = $6
            WHERE id = $1
            RETURNING id
            """
            return await conn.fetchval(UPDATE_SQL, user.id, user.telegram_id, user.name, user.email, user.tokens_used, user.created_at)
        
    
    async def create_message(self, message: Message):
        INSERT_SQL = """
        INSERT INTO Messages (id, text, user_id, source, created_at, channel_id, related_message_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                INSERT_SQL,
                message.id,
                message.text,
                message.user_id,
                message.source,
                message.created_at,
                message.channel_id,
                message.related_message_id
            )
    async def get_messages(self, channel_id: str, count: int) -> List[Message]:
        SELECT_SQL = """
            SELECT * FROM Messages
            WHERE channel_id = $1
            ORDER BY created_at DESC
            LIMIT $2
            """
        async with self.pool.acquire() as conn:
            result = await conn.fetch(SELECT_SQL, channel_id, count)
            messages = [db_record_to_message(record) for record in result]
            return messages
        
    
    async def channel_exists(self, channel_id: str) -> bool:
        """
        Checks if the given channel_id exists in the Channels table.

        Params:
        - channel_id (str): The channel ID to check.

        Returns:
        - bool: True if the channel exists, False otherwise.

        Usage:
        >>> exists = await db_repo.channel_exists("12345")
        >>> print(exists)
        True
        """
        CHECK_SQL = """
            SELECT EXISTS(
                SELECT 1 FROM Channels WHERE id = $1
            )
            """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(CHECK_SQL, channel_id)

    async def create_channel(self, channel_id: str):
        """
        Inserts a new channel ID into the Channels table.

        Params:
        - channel_id (str): The channel ID to insert.

        Usage:
        >>> await db_repo.create_channel("12345")
        """
        INSERT_SQL = """
        INSERT INTO Channels (id)
        VALUES ($1)
        ON CONFLICT (id) DO NOTHING
        """
        async with self.pool.acquire() as conn:
            await conn.execute(INSERT_SQL, channel_id)
