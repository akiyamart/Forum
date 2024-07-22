from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.users.users import user_router, _create_new_user
from src.api.models import ShowUser, UserCreate
from src.database.session import connect_to_db


### User
@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(connect_to_db)) -> ShowUser: 
    return await _create_new_user(body, db)

