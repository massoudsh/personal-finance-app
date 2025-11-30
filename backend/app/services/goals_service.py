"""
Goals service for business logic.
"""
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.goal import Goal, GoalStatus
from app.schemas.goal import GoalCreate, GoalUpdate, GoalWithProgress


class GoalsService:
    """Service for goal operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_goals(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Goal]:
        """Get all goals for a user."""
        return self.db.query(Goal).filter(
            Goal.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_goal(self, goal_id: int, user_id: int) -> Optional[Goal]:
        """Get a specific goal by ID."""
        return self.db.query(Goal).filter(
            Goal.id == goal_id,
            Goal.user_id == user_id
        ).first()
    
    def get_goal_with_progress(
        self,
        goal_id: int,
        user_id: int
    ) -> Optional[GoalWithProgress]:
        """Get goal with progress information."""
        goal = self.get_goal(goal_id, user_id)
        if not goal:
            return None
        
        target = Decimal(str(goal.target_amount))
        current = Decimal(str(goal.current_amount))
        remaining = target - current
        progress_percentage = (current / target * 100) if target > 0 else 0.0
        
        days_remaining = None
        if goal.target_date:
            today = date.today()
            days_remaining = (goal.target_date - today).days
        
        return GoalWithProgress(
            **goal.__dict__,
            progress_percentage=float(progress_percentage),
            remaining_amount=remaining,
            days_remaining=days_remaining
        )
    
    def create_goal(self, goal_data: GoalCreate, user_id: int) -> Goal:
        """Create a new goal."""
        db_goal = Goal(
            **goal_data.model_dump(),
            user_id=user_id
        )
        self.db.add(db_goal)
        self.db.commit()
        self.db.refresh(db_goal)
        return db_goal
    
    def update_goal(
        self,
        goal_id: int,
        goal_data: GoalUpdate,
        user_id: int
    ) -> Optional[Goal]:
        """Update an existing goal."""
        goal = self.get_goal(goal_id, user_id)
        if not goal:
            return None
        
        update_data = goal_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(goal, field, value)
        
        # Auto-complete goal if current_amount >= target_amount
        if Decimal(str(goal.current_amount)) >= Decimal(str(goal.target_amount)):
            goal.status = GoalStatus.COMPLETED
        
        self.db.commit()
        self.db.refresh(goal)
        return goal
    
    def delete_goal(self, goal_id: int, user_id: int) -> bool:
        """Delete a goal."""
        goal = self.get_goal(goal_id, user_id)
        if not goal:
            return False
        
        self.db.delete(goal)
        self.db.commit()
        return True

