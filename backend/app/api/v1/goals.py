"""
Goals API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalUpdate, Goal as GoalSchema, GoalWithProgress
from app.services.goals_service import GoalsService

router = APIRouter()


@router.get("/", response_model=List[GoalSchema])
async def get_goals(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all goals for the current user."""
    service = GoalsService(db)
    return service.get_user_goals(current_user.id, skip=skip, limit=limit)


@router.get("/{goal_id}", response_model=GoalWithProgress)
async def get_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific goal by ID with progress information."""
    service = GoalsService(db)
    goal = service.get_goal_with_progress(goal_id, current_user.id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal


@router.post("/", response_model=GoalSchema, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new goal."""
    service = GoalsService(db)
    return service.create_goal(goal_data, current_user.id)


@router.put("/{goal_id}", response_model=GoalSchema)
async def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing goal."""
    service = GoalsService(db)
    goal = service.update_goal(goal_id, goal_data, current_user.id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a goal."""
    service = GoalsService(db)
    success = service.delete_goal(goal_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

