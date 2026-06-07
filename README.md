# Expense Tracker

## Stack
- **Backend**: FastAPI + SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Streamlit
- **Auth**: JWT tokens

## Quick Start

### 1. Clone and set up backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create .env file
```bash
cp ../.env.example .env
# Edit .env with your values (leave DATABASE_URL blank to use SQLite)
```

### 3. Run the backend
```bash
uvicorn app.main:app --reload --port 8000
# Visit http://localhost:8000/docs to test all endpoints
```

### 4. Run the frontend
```bash
cd ../frontend
streamlit run Home.py
```

## Project Structure
```
expense-tracker/
  backend/
    app/
      api/          ← Route handlers (auth, expenses, income, categories)
      models/       ← SQLAlchemy ORM models
      schemas/      ← Pydantic request/response schemas
      core/         ← database.py, config.py, auth.py
    tests/
    requirements.txt
  frontend/
    pages/          ← Dashboard, Add Expense, History, Add Income
    utils/          ← api.py (HTTP client helper)
  .env.example
  README.md
```
