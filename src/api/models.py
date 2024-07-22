import re
import uuid
from fastapi import HTTPException
from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing import Optional

LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Zа-яА-Я\-]+$")

### User 
class TunedModel(BaseModel): 
    class Config(ConfigDict): 
        from_attributes = True

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
    
class ShowUser(BaseModel): 
    user_id: uuid.UUID
    username: str
    name: str
    surname: str
    email: EmailStr
    is_active: bool
