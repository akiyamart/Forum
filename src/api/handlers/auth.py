from fastapi import Depends, APIRouter, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas.auth import Token
from src.database.session import connect_to_db
from src.api.services.auth.auth import authenticate_user
from src.api.services.tokens.jwt import create_access_token, create_refresh_token
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

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
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = await create_access_token(
        data = {"sub": user.email, "other_data": [user.username, user.name, user.surname]}, expires_delta=access_token_expires
    )
    refresh_token = await create_refresh_token(
        data = {"sub": user.email}, expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token)