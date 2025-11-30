"""
Category schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for category creation."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for category update."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class CategoryInDB(CategoryBase):
    """Category schema with database fields."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Category(CategoryInDB):
    """Category response schema."""
    pass

