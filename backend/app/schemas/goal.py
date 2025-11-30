"""
Goal schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.models.goal import GoalType, GoalStatus


class GoalBase(BaseModel):
    """Base goal schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    goal_type: GoalType
    target_amount: Decimal = Field(..., decimal_places=2)
    current_amount: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    target_date: Optional[date] = None


class GoalCreate(GoalBase):
    """Schema for goal creation."""
    pass


class GoalUpdate(BaseModel):
    """Schema for goal update."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    goal_type: Optional[GoalType] = None
    target_amount: Optional[Decimal] = Field(None, decimal_places=2)
    current_amount: Optional[Decimal] = Field(None, decimal_places=2)
    target_date: Optional[date] = None
    status: Optional[GoalStatus] = None


class GoalInDB(GoalBase):
    """Goal schema with database fields."""
    id: int
    user_id: int
    status: GoalStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Goal(GoalInDB):
    """Goal response schema."""
    pass


class GoalWithProgress(Goal):
    """Goal schema with progress information."""
    progress_percentage: float = Field(default=0.0)
    remaining_amount: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    days_remaining: Optional[int] = None

