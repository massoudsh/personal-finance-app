"""
Dashboard API endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.reports_service import ReportsService

router = APIRouter()


@router.get("/summary")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard summary statistics."""
    service = ReportsService(db)
    return service.get_dashboard_summary(current_user.id)

