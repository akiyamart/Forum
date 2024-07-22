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
    
    async def is_username_taken(self, usernmame: str) -> bool: 
        query = select(User).filter(User.username == usernmame)
        result = await self.db_connect.execute(query)
        user = result.scalars().first()
        return user is not None
    
    async def is_email_taken(self, email: str) -> bool: 
        query = select(User).filter(User.email == email)
        result = await self.db_connect.execute(query)
        user = result.scalars().first()
        return user is not None 