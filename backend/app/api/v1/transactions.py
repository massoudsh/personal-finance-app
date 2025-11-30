"""
Transactions API endpoints.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate, Transaction as TransactionSchema
from app.services.transactions_service import TransactionsService

router = APIRouter()


@router.get("/", response_model=List[TransactionSchema])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    account_id: Optional[int] = None,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all transactions for the current user with optional filters."""
    service = TransactionsService(db)
    return service.get_user_transactions(
        current_user.id,
        skip=skip,
        limit=limit,
        account_id=account_id,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific transaction by ID."""
    service = TransactionsService(db)
    transaction = service.get_transaction(transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.post("/", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new transaction."""
    service = TransactionsService(db)
    return service.create_transaction(transaction_data, current_user.id)


@router.put("/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing transaction."""
    service = TransactionsService(db)
    transaction = service.update_transaction(transaction_id, transaction_data, current_user.id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a transaction."""
    service = TransactionsService(db)
    success = service.delete_transaction(transaction_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

