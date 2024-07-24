from uuid import UUID 
from fastapi import APIRouter
from typing import Union, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.users.models import UserCreate, ShowUserResponse, ShowUserRequest
from src.database.dals import UserDAL
from src.database.models.models import ForumRole, User
from src.api.handlers.auth.hasher import Hasher

user_router = APIRouter()

async def _create_new_user(body: UserCreate, session: AsyncSession) -> Union[ShowUserResponse, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        
        if await user_dal.is_username_taken(body.username) or await user_dal.is_email_taken(body.email): 
            return None
    
        user = await user_dal.create_user(
            username = body.username, 
            name = body.name,
            surname = body.surname,
            email = body.email,
            hashed_password = Hasher.get_password_hash(body.password),
            roles = [ForumRole.ROLE_PORTAL_USER, ]
        )
        return ShowUserResponse(
            user_id = user.user_id,
            username = user.username, 
            name = user.name, 
            surname = user.surname, 
            email = user.email, 
            is_active = user.is_active,
        )

async def _delete_user(user_id: UUID, sesion: AsyncSession) -> Union[UUID, None]: 
    async with sesion.begin(): 
        user_dal = UserDAL(sesion)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id
        )
        return deleted_user_id

async def _update_user(user_id: UUID, updated_user_params: dict, session: AsyncSession) -> Union[UUID, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        if ("username" in updated_user_params and await user_dal.is_username_taken(updated_user_params["username"])
            or 
            "email" in updated_user_params and await user_dal.is_email_taken(updated_user_params["email"])
        ): 
            return None
        updated_user_id = await user_dal.update_user(
            user_id=user_id, 
            **updated_user_params
        )
        return updated_user_id

async def _get_user_by_id(user_id: UUID, session: AsyncSession) -> Union[User, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id
        )
        if user is not None: 
            return user
        
async def _get_user_by_email(email: str, session: AsyncSession) -> Union[User, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        email = await user_dal.get_user_by_email(email=email)
        if email is not None: 
            return email
        
async def _find_user(uuid: Optional[UUID], email: Optional[str], db: AsyncSession) -> Optional[ShowUserResponse]:
    if uuid:
        return await _get_user_by_id(uuid, db)
    elif email:
        return await _get_user_by_email(email, db)
    return None

def _check_user_permissions(target_user: User, current_user: User) -> bool:
    if ForumRole.ROLE_PORTAL_SUPERADMIN in current_user.roles: 
        return False
    if target_user.user_id != current_user.user_id: 
        if not {
            ForumRole.ROLE_PORTAL_ADMIN, 
            ForumRole.ROLE_PORTAL_SUPERADMIN
        }.intersection(current_user.roles):
            return False
        if (
            ForumRole.ROLE_PORTAL_ADMIN in target_user.roles
            and ForumRole.ROLE_PORTAL_ADMIN in current_user.roles
        ):
            return False
        if ForumRole.ROLE_PORTAL_ADMIN in target_user.rolew and ForumRole.ROLE_PORTAL_ADMIN in current_user.roles:
            return False
        return True