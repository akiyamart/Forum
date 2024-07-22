from uuid import UUID 
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from typing import Union 
from src.api.models import UserCreate, ShowUser
from src.database.dals import UserDAL
from src.database.models import ForumRole, User
from src.api.handlers.auth.hasher import Hasher

user_router = APIRouter()

async def _create_new_user(body: UserCreate, session) -> ShowUser: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        if await user_dal.is_username_taken(body.username): 
            raise HTTPException(status_code=409, detail="Username already taken")
        
        user = await user_dal.create_user(
            username = body.username, 
            name = body.name,
            surname = body.surname,
            email = body.email,
            hashed_password = Hasher.get_password_hash(body.password),
            roles = [ForumRole.ROLE_PORTAL_USER, ]
        )
        return ShowUser(
            user_id = user.user_id,
            username = user.username, 
            name = user.name, 
            surname = user.surname, 
            email = user.email, 
            is_active = user.is_active,
        )
