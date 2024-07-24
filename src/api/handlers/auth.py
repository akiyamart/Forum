from fastapi import Depends, APIRouter, HTTPException, status
from uuid import UUID
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.services.users.users import create_new_user, get_user_by_id, find_user, delete_user, update_user, check_user_permissions
from src.api.schemas.users import ShowUserResponse, UserCreate, DeletedUserResponse, UpdatedUserResponse, UpdatedUserRequest
from src.api.schemas.auth import Token
from src.database.session import connect_to_db
from src.api.services.auth.auth import get_current_user_from_token
from src.api.services.auth.auth import authenticate_user, create_access_token, get_current_user_from_token
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES

login_router = APIRouter()

@login_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(connect_to_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"subj": user.email, "other_data": [user.name, user.surname, user.surname]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}