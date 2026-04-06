from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.models.user import UserRole


class UserCreate(BaseModel):
    username:  str
    email:     EmailStr
    password:  str
    full_name: Optional[str] = None
    role:      UserRole = UserRole.viewer

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v


class UserUpdate(BaseModel):
    username:  Optional[str]      = None
    email:     Optional[EmailStr] = None
    full_name: Optional[str]      = None
    role:      Optional[UserRole] = None


class UserResponse(BaseModel):
    id:         int
    username:   str
    email:      str
    full_name:  Optional[str] = None
    role:       UserRole
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
