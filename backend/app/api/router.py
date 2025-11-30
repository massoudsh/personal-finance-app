"""
API router configuration.
"""
from fastapi import APIRouter
from app.api.v1 import auth, accounts, transactions, budgets, goals, dashboard, reports

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])

