"""
Transactions service for business logic.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from decimal import Decimal


class TransactionsService:
    """Service for transaction operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_transactions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Transaction]:
        """Get all transactions for a user with optional filters."""
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        return query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    
    def get_transaction(self, transaction_id: int, user_id: int) -> Optional[Transaction]:
        """Get a specific transaction by ID."""
        return self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
    
    def create_transaction(
        self,
        transaction_data: TransactionCreate,
        user_id: int
    ) -> Transaction:
        """Create a new transaction and update account balance."""
        # Verify account belongs to user
        account = self.db.query(Account).filter(
            Account.id == transaction_data.account_id,
            Account.user_id == user_id
        ).first()
        
        if not account:
            raise ValueError("Account not found")
        
        db_transaction = Transaction(
            **transaction_data.model_dump(),
            user_id=user_id
        )
        
        # Update account balance
        amount = Decimal(str(transaction_data.amount))
        if transaction_data.transaction_type.value == "income":
            account.balance += amount
        elif transaction_data.transaction_type.value == "expense":
            account.balance -= amount
        
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    
    def update_transaction(
        self,
        transaction_id: int,
        transaction_data: TransactionUpdate,
        user_id: int
    ) -> Optional[Transaction]:
        """Update an existing transaction."""
        transaction = self.get_transaction(transaction_id, user_id)
        if not transaction:
            return None
        
        # Handle balance updates if amount or type changes
        old_amount = transaction.amount
        old_type = transaction.transaction_type
        
        update_data = transaction_data.model_dump(exclude_unset=True)
        
        # Update transaction
        for field, value in update_data.items():
            setattr(transaction, field, value)
        
        # Revert old transaction impact on balance
        account = transaction.account
        if old_type.value == "income":
            account.balance -= Decimal(str(old_amount))
        elif old_type.value == "expense":
            account.balance += Decimal(str(old_amount))
        
        # Apply new transaction impact on balance
        new_amount = Decimal(str(transaction.amount))
        if transaction.transaction_type.value == "income":
            account.balance += new_amount
        elif transaction.transaction_type.value == "expense":
            account.balance -= new_amount
        
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def delete_transaction(self, transaction_id: int, user_id: int) -> bool:
        """Delete a transaction and update account balance."""
        transaction = self.get_transaction(transaction_id, user_id)
        if not transaction:
            return False
        
        # Revert balance change
        account = transaction.account
        amount = Decimal(str(transaction.amount))
        if transaction.transaction_type.value == "income":
            account.balance -= amount
        elif transaction.transaction_type.value == "expense":
            account.balance += amount
        
        self.db.delete(transaction)
        self.db.commit()
        return True

