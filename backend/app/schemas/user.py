"""
User schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for user update."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """User schema with database fields."""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class User(UserInDB):
    """User response schema."""
    pass


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""
    user_id: Optional[int] = None


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str

