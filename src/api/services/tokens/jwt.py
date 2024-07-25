from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS
from src.database.session import connect_to_db
from src.api.services.users.users import get_user_by_email

def extract_token_from_headers(auth: str) -> str: 
    try: 
        _, token = auth.split()
        return token
    except ValueError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid headers")

def decode_jwt_token(token: str, secret_key: str, algorithms: list) -> str:
    try: 
        payload = jwt.decode(token, secret_key, algorithms) 
        return payload
    except: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): 
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now() + expires_delta
    else: 
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

async def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None): 
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now() + expires_delta
    else: 
        expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Middleware
async def refresh_access_token(request: Request, call_next):
    public_paths = ["/login", "/register", "/openapi.json", "/docs"]

    if request.url.path in public_paths:
        response = await call_next(request)
        return response
    
    auth: str = request.headers.get("Authorization")
    if auth: 
        access_token =  extract_token_from_headers(auth)
        try: 
            payload =  decode_jwt_token(access_token, SECRET_KEY, [ALGORITHM])
            request.state.user_email = payload.get("sub")
        except HTTPException: 
            refresh_token = request.cookies.get("refresh_token")
            if refresh_token:
                try:
                    payload =  decode_jwt_token(access_token, SECRET_KEY, [ALGORITHM])
                    email: str = payload.get("sub")
                    if email:
                        async with connect_to_db() as session: 
                            user = await get_user_by_email(email=email, session=session)
                            if user:
                                new_access_token = await create_access_token({"sub": user.email})
                                response = await call_next(request)
                                response.set_cookie(key="access_token", value=f"Bearer {new_access_token}")
                                return response
                except HTTPException:
                    return JSONResponse(status_code=401, content={"detail": "Invalid refresh token"})
            return JSONResponse(status_code=401, content={"detail": "Invalid access token"})
    response = await call_next(request)
    return response
                        