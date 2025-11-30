"""
Forecast service for financial forecasting.
"""
from typing import Dict, List
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction, TransactionType


class ForecastService:
    """Service for financial forecasting."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def forecast_monthly_expenses(
        self,
        user_id: int,
        months: int = 3
    ) -> List[Dict]:
        """Forecast monthly expenses based on historical data."""
        # Get average monthly expenses from last 6 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)  # 6 months
        
        avg_monthly = self.db.query(func.avg(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).scalar() or Decimal("0.00")
        
        forecasts = []
        for i in range(months):
            forecast_date = end_date + timedelta(days=30 * (i + 1))
            forecasts.append({
                "month": forecast_date.strftime("%Y-%m"),
                "forecasted_amount": float(avg_monthly)
            })
        
        return forecasts

