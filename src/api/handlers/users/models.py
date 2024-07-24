import re
import uuid
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional

LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Zа-яА-Я\-]+$")

class UserCreate(BaseModel):
    username: str
    name: str
    surname: str 
    email: EmailStr
    password: str

    @field_validator("name", mode="before")
    @staticmethod
    def validate_name(value): 
        if not LETTER_MATCH_PATTERN.match(value): 
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value
    
    @field_validator("surname", mode="before")
    @staticmethod
    def validate_surname(value): 
        if not LETTER_MATCH_PATTERN.match(value): 
            raise HTTPException(
                status_code=422, detail="Surname should contain only letters"
            )
        return value
    
class UpdatedUserRequest(BaseModel): 
    username: Optional[str] = Field(None, min_length=3)
    name: Optional[str] = Field(None, min_length=1)
    surname: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = Field(None, min_length=2)

    @field_validator("name", mode="before")
    @staticmethod
    def validate_name(value): 
        if not LETTER_MATCH_PATTERN.match(value): 
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value
    
    @field_validator("surname", mode="before")
    @staticmethod
    def validate_surname(value): 
        if not LETTER_MATCH_PATTERN.match(value): 
            raise HTTPException(
                status_code=422, detail="Surname should contain only letters"
            )
        return value
    
class ShowUserRequest(BaseModel):
    uuid: Optional[uuid.UUID]
    email: Optional[EmailStr]

class ShowUserResponse(BaseModel): 
    user_id: uuid.UUID
    username: str
    name: str
    surname: str
    email: EmailStr
    is_active: bool

class DeletedUserResponse(BaseModel): 
    deleted_user_id: uuid.UUID

class UpdatedUserResponse(BaseModel): 
    updated_user_id: uuid.UUID

# Потом убрать из models.py в другой файл (какой-нибудь новый)
class SearchKey(BaseModel): 
    pass