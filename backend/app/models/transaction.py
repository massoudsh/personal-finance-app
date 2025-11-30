"""
Transaction model for financial transactions.
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class TransactionType(str, enum.Enum):
    """Transaction type enumeration."""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class Transaction(Base):
    """Transaction model."""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type}, date={self.date})>"

