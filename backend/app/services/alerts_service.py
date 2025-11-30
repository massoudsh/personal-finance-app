"""
Alerts service for budget alerts and notifications.
"""
from typing import List, Dict
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType


class AlertsService:
    """Service for alerts and notifications."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_budget_alerts(self, user_id: int) -> List[Dict]:
        """Get budget alerts for user."""
        alerts = []
        budgets = self.db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.is_active == True
        ).all()
        
        for budget in budgets:
            # Calculate spending
            spent = self.db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.date >= budget.start_date
            )
            
            if budget.end_date:
                spent = spent.filter(Transaction.date <= budget.end_date)
            
            if budget.category_id:
                spent = spent.filter(Transaction.category_id == budget.category_id)
            
            spent_amount = spent.scalar() or Decimal("0.00")
            percentage = (spent_amount / Decimal(str(budget.amount)) * 100) if budget.amount > 0 else 0
            
            # Alert if over 80% of budget
            if percentage >= 80:
                alerts.append({
                    "budget_id": budget.id,
                    "budget_name": budget.name,
                    "spent": float(spent_amount),
                    "budget_amount": float(budget.amount),
                    "percentage": float(percentage),
                    "alert_type": "warning" if percentage < 100 else "critical"
                })
        
        return alerts

