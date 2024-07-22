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
        if await user_dal.is_email_taken(body.email): 
            raise HTTPException(status_code=409, detail="Email already taken")
        
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

async def _delete_user(user_id: UUID, sesion) -> Union[UUID, None]: 
    async with sesion.begin(): 
        user_dal = UserDAL(sesion)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id
        )
        return deleted_user_id

async def _update_user(user_id: UUID, updated_user_params: dict, session) -> Union[UUID, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, 
            **updated_user_params
        )
        return updated_user_id

async def _get_user_by_id(user_id: UUID, session) -> Union[User, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        user = user_dal.get_user_by_id(
            user_id=user_id
        )
        if user is not None: 
            return user
        
async def _get_user_by_email(email, session) -> Union[User, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        email = await user_dal.get_user_by_email(email=email)
        if email is not None: 
            return email