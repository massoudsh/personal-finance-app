# System Architecture

## Overview
The application follows a three-tier architecture: Frontend (Next.js), Backend (FastAPI), and Database (PostgreSQL).

## Architecture Diagram

```
┌─────────────────┐
│   Next.js App   │
│   (Frontend)    │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   FastAPI API   │
│   (Backend)     │
└────────┬────────┘
         │ SQL
         │
┌────────▼────────┐
│   PostgreSQL    │
│   (Database)    │
└─────────────────┘
```

## Components

### Frontend (Next.js)
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context / Zustand
- **API Client**: Fetch API with custom wrapper
- **Validation**: Zod schemas
- **Charts**: Recharts

### Backend (FastAPI)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Database**: PostgreSQL

### Database
- **Type**: PostgreSQL 15+
- **ORM**: SQLAlchemy
- **Migrations**: Alembic (recommended)

## Layer Structure

### Backend Layers

1. **API Layer** (`app/api/v1/`)
   - HTTP endpoints
   - Request/response handling
   - Authentication checks

2. **Service Layer** (`app/services/`)
   - Business logic
   - Data processing
   - Complex operations

3. **Model Layer** (`app/models/`)
   - Database models
   - Relationships
   - Data access

4. **Schema Layer** (`app/schemas/`)
   - Request validation
   - Response serialization
   - Data transformation

### Frontend Layers

1. **Pages** (`app/`)
   - Route handlers
   - Page components
   - Server/client components

2. **Components** (`components/`)
   - Reusable UI components
   - Layout components
   - Form components
   - Chart components

3. **Lib** (`lib/`)
   - API client
   - Utilities
   - Helpers

## Data Flow

1. User interacts with frontend
2. Frontend makes API request to backend
3. Backend validates request (schema)
4. Backend checks authentication (JWT)
5. Backend executes business logic (service)
6. Backend queries database (model)
7. Backend formats response (schema)
8. Frontend receives and displays data

## Security

- JWT tokens for authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation at API and schema levels
- SQL injection prevention via ORM
- Environment variables for secrets

## Deployment

### Development
- Backend: `uvicorn app.main:app --reload`
- Frontend: `npm run dev`
- Database: Local PostgreSQL or Docker

### Production
- Backend: Docker container with uvicorn
- Frontend: Next.js static export or Vercel
- Database: Managed PostgreSQL (AWS RDS, Supabase, etc.)
- Reverse Proxy: Nginx (optional)

## Scalability Considerations

- Database connection pooling
- API rate limiting
- Caching layer (Redis) - future
- Background jobs (Celery) - future
- CDN for static assets - future

