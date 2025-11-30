# Database Design

## Overview
PostgreSQL database with SQLAlchemy ORM. All tables include `created_at` and `updated_at` timestamps.

## Tables

### users
- `id` (PK, Integer)
- `email` (String, Unique, Indexed)
- `username` (String, Unique, Indexed)
- `hashed_password` (String)
- `full_name` (String, Nullable)
- `is_active` (Boolean, Default: True)
- `is_superuser` (Boolean, Default: False)
- `created_at` (DateTime)
- `updated_at` (DateTime, Nullable)

### accounts
- `id` (PK, Integer)
- `user_id` (FK -> users.id)
- `name` (String)
- `account_type` (Enum: checking, savings, credit_card, investment, loan, other)
- `balance` (Numeric(10,2), Default: 0.00)
- `currency` (String, Default: "USD")
- `description` (String, Nullable)
- `is_active` (Boolean, Default: True)
- `created_at` (DateTime)
- `updated_at` (DateTime, Nullable)

### categories
- `id` (PK, Integer)
- `name` (String, Indexed)
- `description` (String, Nullable)
- `color` (String, Nullable) - Hex color for UI
- `icon` (String, Nullable) - Icon name for UI
- `created_at` (DateTime)

### transactions
- `id` (PK, Integer)
- `user_id` (FK -> users.id)
- `account_id` (FK -> accounts.id)
- `category_id` (FK -> categories.id, Nullable)
- `amount` (Numeric(10,2))
- `transaction_type` (Enum: income, expense, transfer)
- `description` (Text, Nullable)
- `date` (DateTime, Indexed)
- `notes` (Text, Nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime, Nullable)

### budgets
- `id` (PK, Integer)
- `user_id` (FK -> users.id)
- `category_id` (FK -> categories.id, Nullable)
- `name` (String)
- `amount` (Numeric(10,2))
- `period` (Enum: weekly, monthly, yearly, Default: monthly)
- `start_date` (Date)
- `end_date` (Date, Nullable)
- `is_active` (Boolean, Default: True)
- `created_at` (DateTime)
- `updated_at` (DateTime, Nullable)

### goals
- `id` (PK, Integer)
- `user_id` (FK -> users.id)
- `name` (String)
- `description` (String, Nullable)
- `goal_type` (Enum: savings, debt_payoff, purchase, emergency_fund, other)
- `target_amount` (Numeric(10,2))
- `current_amount` (Numeric(10,2), Default: 0.00)
- `target_date` (Date, Nullable)
- `status` (Enum: active, completed, paused, cancelled, Default: active)
- `created_at` (DateTime)
- `updated_at` (DateTime, Nullable)

## Relationships

- User -> Accounts (One-to-Many)
- User -> Transactions (One-to-Many)
- User -> Budgets (One-to-Many)
- User -> Goals (One-to-Many)
- Account -> Transactions (One-to-Many)
- Category -> Transactions (One-to-Many)
- Category -> Budgets (One-to-Many)

## Indexes

- `users.email` - Unique index
- `users.username` - Unique index
- `transactions.date` - Index for date filtering
- `categories.name` - Index for category lookup

## Constraints

- Account balance cannot be negative (enforced at application level)
- Transaction amount must be positive
- Budget amount must be positive
- Goal target_amount must be positive

