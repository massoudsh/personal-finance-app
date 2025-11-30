"""
Goal model for financial goals.
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class GoalType(str, enum.Enum):
    """Goal type enumeration."""
    SAVINGS = "savings"
    DEBT_PAYOFF = "debt_payoff"
    PURCHASE = "purchase"
    EMERGENCY_FUND = "emergency_fund"
    OTHER = "other"


class GoalStatus(str, enum.Enum):
    """Goal status enumeration."""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class Goal(Base):
    """Goal model."""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    goal_type = Column(Enum(GoalType), nullable=False)
    target_amount = Column(Numeric(10, 2), nullable=False)
    current_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    target_date = Column(Date, nullable=True)
    status = Column(Enum(GoalStatus), nullable=False, default=GoalStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="goals")
    
    def __repr__(self):
        return f"<Goal(id={self.id}, name={self.name}, target_amount={self.target_amount}, status={self.status})>"

