"""
Budget schemas for request/response validation.
"""
from pydantic import BaseModel, Field, condecimal
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.models.budget import BudgetPeriod

Money = condecimal(max_digits=10, decimal_places=2)


class BudgetBase(BaseModel):
    """Base budget schema."""
    category_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    amount: Money
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
    amount: Optional[Money] = None
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
    spent: Money = Decimal("0.00")
    remaining: Money = Decimal("0.00")
    percentage_used: float = Field(default=0.0)

