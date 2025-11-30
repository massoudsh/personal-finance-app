"""
Category model for transaction categorization.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Category(Base):
    """Category model for transactions."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    color = Column(String, nullable=True)  # Hex color code for UI
    icon = Column(String, nullable=True)  # Icon name for UI
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

