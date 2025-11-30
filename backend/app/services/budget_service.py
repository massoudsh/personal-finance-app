"""
Budget service for business logic.
"""
from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from decimal import Decimal
from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetWithSpending


class BudgetService:
    """Service for budget operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_budgets(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Budget]:
        """Get all budgets for a user."""
        return self.db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_budget(self, budget_id: int, user_id: int) -> Optional[Budget]:
        """Get a specific budget by ID."""
        return self.db.query(Budget).filter(
            Budget.id == budget_id,
            Budget.user_id == user_id
        ).first()
    
    def get_budget_with_spending(
        self,
        budget_id: int,
        user_id: int
    ) -> Optional[BudgetWithSpending]:
        """Get budget with spending information."""
        budget = self.get_budget(budget_id, user_id)
        if not budget:
            return None
        
        # Calculate spending for the budget period
        spent = self._calculate_spending(budget, user_id)
        remaining = Decimal(str(budget.amount)) - spent
        percentage_used = (spent / Decimal(str(budget.amount)) * 100) if budget.amount > 0 else 0
        
        return BudgetWithSpending(
            **budget.__dict__,
            spent=spent,
            remaining=remaining,
            percentage_used=float(percentage_used)
        )
    
    def _calculate_spending(self, budget: Budget, user_id: int) -> Decimal:
        """Calculate spending for a budget."""
        query = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE,
            Transaction.date >= budget.start_date
        )
        
        if budget.end_date:
            query = query.filter(Transaction.date <= budget.end_date)
        
        if budget.category_id:
            query = query.filter(Transaction.category_id == budget.category_id)
        
        result = query.scalar()
        return Decimal(str(result)) if result else Decimal("0.00")
    
    def create_budget(self, budget_data: BudgetCreate, user_id: int) -> Budget:
        """Create a new budget."""
        db_budget = Budget(
            **budget_data.model_dump(),
            user_id=user_id
        )
        self.db.add(db_budget)
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget
    
    def update_budget(
        self,
        budget_id: int,
        budget_data: BudgetUpdate,
        user_id: int
    ) -> Optional[Budget]:
        """Update an existing budget."""
        budget = self.get_budget(budget_id, user_id)
        if not budget:
            return None
        
        update_data = budget_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(budget, field, value)
        
        self.db.commit()
        self.db.refresh(budget)
        return budget
    
    def delete_budget(self, budget_id: int, user_id: int) -> bool:
        """Delete a budget."""
        budget = self.get_budget(budget_id, user_id)
        if not budget:
            return False
        
        self.db.delete(budget)
        self.db.commit()
        return True

