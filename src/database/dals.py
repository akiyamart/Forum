from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union 
from sqlalchemy import update, and_, select
from uuid import UUID
from src.database.models import User, ForumRole


class UserDAL:
    def __init__(self, db_connect: AsyncSession):
        self.db_connect = db_connect

    async def create_user(
            self, username: str, name: str, surname: str, email: str, hashed_password: str, roles: list[ForumRole]
    ) -> User: 
        new_user = User(
            username=username, 
            name=name, 
            surname=surname,
            email=email, 
            hashed_password=hashed_password,
            roles=roles
        )
        self.db_connect.add(new_user)
        await self.db_connect.flush()
        return new_user