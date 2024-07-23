from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union 
from sqlalchemy import update, and_, select
from uuid import UUID
from src.database.models.models import User, ForumRole


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
    
    async def delete_user(self, user_id: UUID) -> Union[UUID, None]: 
        query = update(User). \
                where(and_(User.user_id == user_id, User.is_active == True)). \
                values(is_active=False). \
                returning(User.user_id)
        result = await self.db_connect.execute(query)
        deleted_user_id = result.fetchone()
        if deleted_user_id is not None: 
            return deleted_user_id[0]
        
    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]: 
        query = update(User). \
                where(and_(User.user_id == user_id, User.is_active == True)). \
                values(kwargs). \
                returning(User.user_id)
        result = await self.db_connect.execute(query)
        updated_user_id_row = result.fetchone()
        if updated_user_id_row is not None: 
            return updated_user_id_row[0]
        
    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]: 
        query = select(User).where(User.user_id == user_id)
        result = await self.db_connect.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]
                
    async def get_user_by_email(self, email: str) -> Union[User, None]: 
        query = select(User).where(User.email == email)
        result = await self.db_connect.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]