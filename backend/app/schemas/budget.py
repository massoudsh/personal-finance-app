"""
Budget schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.models.budget import BudgetPeriod


class BudgetBase(BaseModel):
    """Base budget schema."""
    category_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., decimal_places=2)
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    start_date: date
    end_date: Optional[date] = None


class BudgetCreate(BudgetBase):
    """Schema for budget creation."""
    pass


class BudgetUpdate(BaseModel):
    """Schema for budget update."""
    category_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[Decimal] = Field(None, decimal_places=2)
    period: Optional[BudgetPeriod] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


class BudgetInDB(BudgetBase):
    """Budget schema with database fields."""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Budget(BudgetInDB):
    """Budget response schema."""
    pass


class BudgetWithSpending(Budget):
    """Budget schema with spending information."""
    spent: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    remaining: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    percentage_used: float = Field(default=0.0)

