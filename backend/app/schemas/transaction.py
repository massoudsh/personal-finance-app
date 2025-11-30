"""
Transaction schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    """Base transaction schema."""
    account_id: int
    category_id: Optional[int] = None
    amount: Decimal = Field(..., decimal_places=2)
    transaction_type: TransactionType
    description: Optional[str] = None
    date: datetime
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Schema for transaction creation."""
    pass


class TransactionUpdate(BaseModel):
    """Schema for transaction update."""
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, decimal_places=2)
    transaction_type: Optional[TransactionType] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None


class TransactionInDB(TransactionBase):
    """Transaction schema with database fields."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Transaction(TransactionInDB):
    """Transaction response schema."""
    pass

