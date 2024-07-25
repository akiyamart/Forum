from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import status 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from src.database.session import connect_to_db
from src.database.dals import UserDAL
from src.api.services.auth.hasher import Hasher
from src.config import SECRET_KEY, ALGORITHM

login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def _get_user_by_email_for_auth(email: str, session: AsyncSession): 
    async with session.begin(): 
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(
            email=email
        )

async def authenticate_user(email: str, password: str, db: AsyncSession): 
    user = await _get_user_by_email_for_auth(email, db)
    if user is None: 
        return
    if not Hasher.verify_password(password, user.hashed_password): 
        return 
    return user

async def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(connect_to_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials"
    ) 
    try: 
        payload = jwt.decode(
            token=token, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None: 
            raise credentials_exception
    except JWTError: 
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None: 
        raise HTTPException(status_code=500, detail="")
    return user

