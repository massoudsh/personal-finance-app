"""
Budgets API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetUpdate, Budget as BudgetSchema, BudgetWithSpending
from app.services.budget_service import BudgetService

router = APIRouter()


@router.get("/", response_model=List[BudgetSchema])
async def get_budgets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all budgets for the current user."""
    service = BudgetService(db)
    return service.get_user_budgets(current_user.id, skip=skip, limit=limit)


@router.get("/{budget_id}", response_model=BudgetWithSpending)
async def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific budget by ID with spending information."""
    service = BudgetService(db)
    budget = service.get_budget_with_spending(budget_id, current_user.id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget


@router.post("/", response_model=BudgetSchema, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new budget."""
    service = BudgetService(db)
    return service.create_budget(budget_data, current_user.id)


@router.put("/{budget_id}", response_model=BudgetSchema)
async def update_budget(
    budget_id: int,
    budget_data: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing budget."""
    service = BudgetService(db)
    budget = service.update_budget(budget_id, budget_data, current_user.id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a budget."""
    service = BudgetService(db)
    success = service.delete_budget(budget_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

