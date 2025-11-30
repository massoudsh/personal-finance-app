"""
Budget model for budget management.
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class BudgetPeriod(str, enum.Enum):
    """Budget period enumeration."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Budget(Base):
    """Budget model."""
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    name = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    period = Column(Enum(BudgetPeriod), nullable=False, default=BudgetPeriod.MONTHLY)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")
    
    def __repr__(self):
        return f"<Budget(id={self.id}, name={self.name}, amount={self.amount}, period={self.period})>"

