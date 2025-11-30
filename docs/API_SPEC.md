# API Specification

## Base URL
`http://localhost:8000/api/v1`

## Authentication
All endpoints except `/auth/register` and `/auth/login` require authentication via Bearer token.

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register
- **POST** `/auth/register`
- **Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "Full Name"
}
```

#### Login
- **POST** `/auth/login`
- **Body:** (form-data)
  - `username`: string
  - `password`: string
- **Response:**
```json
{
  "access_token": "token",
  "refresh_token": "token",
  "token_type": "bearer"
}
```

#### Refresh Token
- **POST** `/auth/refresh`
- **Body:**
```json
{
  "refresh_token": "token"
}
```

#### Get Current User
- **GET** `/auth/me`
- **Headers:** Authorization Bearer token

### Accounts

#### List Accounts
- **GET** `/accounts?skip=0&limit=100`

#### Get Account
- **GET** `/accounts/{id}`

#### Create Account
- **POST** `/accounts`
- **Body:**
```json
{
  "name": "Checking Account",
  "account_type": "checking",
  "balance": 1000.00,
  "currency": "USD",
  "description": "Main checking account"
}
```

#### Update Account
- **PUT** `/accounts/{id}`
- **Body:** (partial update)

#### Delete Account
- **DELETE** `/accounts/{id}`

### Transactions

#### List Transactions
- **GET** `/transactions?skip=0&limit=100&account_id=1&category_id=2&start_date=2024-01-01&end_date=2024-12-31`

#### Get Transaction
- **GET** `/transactions/{id}`

#### Create Transaction
- **POST** `/transactions`
- **Body:**
```json
{
  "account_id": 1,
  "category_id": 2,
  "amount": 50.00,
  "transaction_type": "expense",
  "description": "Grocery shopping",
  "date": "2024-01-15T10:00:00Z",
  "notes": "Weekly groceries"
}
```

#### Update Transaction
- **PUT** `/transactions/{id}`

#### Delete Transaction
- **DELETE** `/transactions/{id}`

### Budgets

#### List Budgets
- **GET** `/budgets?skip=0&limit=100`

#### Get Budget
- **GET** `/budgets/{id}` (includes spending info)

#### Create Budget
- **POST** `/budgets`
- **Body:**
```json
{
  "category_id": 2,
  "name": "Monthly Groceries",
  "amount": 500.00,
  "period": "monthly",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

#### Update Budget
- **PUT** `/budgets/{id}`

#### Delete Budget
- **DELETE** `/budgets/{id}`

### Goals

#### List Goals
- **GET** `/goals?skip=0&limit=100`

#### Get Goal
- **GET** `/goals/{id}` (includes progress info)

#### Create Goal
- **POST** `/goals`
- **Body:**
```json
{
  "name": "Emergency Fund",
  "description": "Build 6 months emergency fund",
  "goal_type": "savings",
  "target_amount": 10000.00,
  "current_amount": 2000.00,
  "target_date": "2024-12-31"
}
```

#### Update Goal
- **PUT** `/goals/{id}`

#### Delete Goal
- **DELETE** `/goals/{id}`

### Dashboard

#### Get Summary
- **GET** `/dashboard/summary`
- **Response:**
```json
{
  "total_balance": 5000.00,
  "month_income": 3000.00,
  "month_expenses": 2000.00,
  "month_net": 1000.00,
  "active_budgets": 5,
  "active_goals": 3,
  "recent_transactions": [...]
}
```

### Reports

#### Expenses by Category
- **GET** `/reports/expenses-by-category?start_date=2024-01-01&end_date=2024-12-31`

#### Income vs Expenses
- **GET** `/reports/income-vs-expenses?start_date=2024-01-01&end_date=2024-12-31`

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message"
}
```

### Status Codes
- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

