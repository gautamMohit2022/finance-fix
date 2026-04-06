<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0f23,50:1a1a3e,100:0d1117&height=200&section=header&text=FinTrack&fontSize=80&fontColor=00d4ff&fontAlignY=38&desc=Production-Grade%20Finance%20Tracking%20System&descAlignY=58&descColor=a0aec0&animation=fadeIn" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![Netlify](https://img.shields.io/badge/Deployed-Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://fintrack-analytics.netlify.app)

<br/>

> **A production-grade Python finance tracking backend** with role-based access control, live analytics, budget tracking, and a fully connected dark-themed frontend dashboard — built for Zorvyn FinTech Pvt. Ltd.

<br/>

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-fintrack--analytics.netlify.app-00d4ff?style=for-the-badge)](https://fintrack-analytics.netlify.app/pages/login.html)
[![API Docs](https://img.shields.io/badge/📮%20Postman%20Docs-View%20Collection-FF6C37?style=for-the-badge)](https://documenter.getpostman.com/view/53769985/2sBXiqEoRf)
[![Swagger UI](https://img.shields.io/badge/📖%20Swagger%20UI-localhost:8000/docs-85EA2D?style=for-the-badge)](http://127.0.0.1:8000/docs)

</div>

---

## 📸 Screenshots

<div align="center">

| Dashboard | 
<img width="1917" height="908" alt="Screenshot 2026-04-06 190825" src="https://github.com/user-attachments/assets/515b0fa3-a39b-4a7a-84ee-eca0805834a8" />

| Transactions |
<img width="1919" height="917" alt="Screenshot 2026-04-06 191441" src="https://github.com/user-attachments/assets/b5ff549a-4be9-4cc8-b6c6-892510861d09" />


| Analytics | 
<img width="1917" height="902" alt="Screenshot 2026-04-06 191848" src="https://github.com/user-attachments/assets/7346cb55-0dde-43d6-aed4-444b512288b7" />
 

| Budget Tracker |
<img width="1919" height="889" alt="Screenshot 2026-04-06 191528" src="https://github.com/user-attachments/assets/62dea62d-0bcb-49d0-ab18-20b9c0b06ba7" />


| User Management |
<img width="1909" height="868" alt="Screenshot 2026-04-06 191518" src="https://github.com/user-attachments/assets/f3f7f0a9-3676-4750-9745-329b1ed23dca" />


 [the live demo](https://fintrack-analytics.netlify.app)*

</div>

---



## 🧭 Overview

**FinTrack** is a full-stack personal finance management system engineered for correctness, security, and extensibility. It supports three user roles with distinct privileges, enforced at the API layer — not just the UI.

### What makes this stand out

| Feature | Detail |
|---|---|
| 🔐 **True RBAC** | Roles enforced via FastAPI `Depends()` — bypassing the UI still returns `403` |
| 📊 **8 Analytics Endpoints** | Complete summary system covering income, expenses, trends, category breakdowns |
| 🗑️ **Soft Delete** | Transactions are never permanently lost — audit trail preserved |
| 🌐 **Full Frontend** | Dark-themed dashboard with live charts, filters, and real-time backend data |
| 🌱 **Seed Script** | One command populates 60 realistic transactions across 6 months |
| 💰 **Budget Tracking** | Per-category budget limits with spending vs. limit status |

---

## 🛠 Tech Stack

<div align="center">

| Layer | Technology | Reason |
|:------|:-----------|:-------|
| **Backend Framework** | FastAPI 0.100+ | Async, auto-docs, Pydantic validation built-in |
| **Database** | PostgreSQL 15+ | Production-grade relational DB with indexing |
| **ORM** | SQLAlchemy 2.0 | Clean typed model definitions, relationship support |
| **Auth** | JWT + bcrypt | Stateless tokens, industry-standard hashing |
| **Validation** | Pydantic v2 | Schema-level validation with clear error messages |
| **Frontend** | HTML / CSS / Vanilla JS | Zero build tooling, no framework dependency |
| **Charts** | Chart.js | Lightweight, responsive, well-documented |
| **Deployment** | Netlify (frontend) | Static hosting with instant CDN distribution |

</div>

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                         │
│         HTML / CSS / Vanilla JS  ·  Chart.js                │
│     Login · Dashboard · Analytics · Budget · Users          │
└──────────────────────┬──────────────────────────────────────┘
                       │  HTTP / JWT Bearer Token
┌──────────────────────▼──────────────────────────────────────┐
│                      API LAYER  (FastAPI)                    │
│                                                             │
│   ┌──────────┐  ┌─────────────┐  ┌─────────┐  ┌────────┐  │
│   │  /auth   │  │/transactions│  │/summary │  │/budget │  │
│   └──────────┘  └─────────────┘  └─────────┘  └────────┘  │
│                                                             │
│          Dependency Injection → require_role()              │
│         Viewer ──► Analyst ──────────► Admin                │
└──────────────────────┬──────────────────────────────────────┘
                       │  SQLAlchemy ORM
┌──────────────────────▼──────────────────────────────────────┐
│                   DATABASE LAYER (PostgreSQL)                │
│          users  ·  transactions  ·  budgets                 │
│              Foreign keys · Soft delete · Indexes           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
finance-fix/
│
├── app/
│   ├── auth/
│   │   ├── dependencies.py        # get_current_user, require_role factory
│   │   ├── jwt_handler.py         # JWT create + decode
│   │   └── password.py            # bcrypt hash + verify
│   │
│   ├── models/
│   │   ├── user.py                # User model + UserRole enum
│   │   ├── transaction.py         # Transaction model + soft delete
│   │   └── budget.py              # Budget model per category
│   │
│   ├── routers/
│   │   ├── auth.py                # POST /auth/register, /auth/login
│   │   ├── transactions.py        # Full CRUD + filters + pagination
│   │   ├── summary.py             # 8 analytics endpoints
│   │   ├── budget.py              # Budget CRUD + spending status
│   │   └── users.py               # User management (admin only)
│   │
│   ├── schemas/
│   │   ├── user.py                # UserCreate, UserResponse, Token
│   │   ├── transaction.py         # TransactionCreate, Update, Paginated
│   │   └── budget.py              # BudgetCreate, BudgetResponse
│   │
│   ├── services/
│   │   ├── transaction_service.py # CRUD + filter business logic
│   │   ├── summary_service.py     # All 8 summary computations
│   │   └── budget_service.py      # Budget + spending vs limit
│   │
│   ├── config.py                  # Env config (DATABASE_URL, SECRET_KEY)
│   ├── database.py                # SQLAlchemy engine + session
│   └── main.py                    # FastAPI app, CORS, routes, startup
│
├── frontend/
│   ├── assets/
│   │   ├── css/style.css          # Complete design system (dark theme)
│   │   └── js/
│   │       ├── api.js             # All API calls centralized
│   │       ├── auth.js            # Token management + localStorage
│   │       ├── sidebar.js         # Role-aware sidebar initializer
│   │       └── utils.js           # Currency, dates, toasts, helpers
│   └── pages/
│       ├── login.html             # JWT login with role tabs
│       ├── register.html          # User registration
│       ├── dashboard.html         # Financial overview + charts
│       ├── transaction.html       # CRUD + filters + pagination
│       ├── budget.html            # Budget tracker
│       ├── summary.html           # All 6 summaries + API reference
│       ├── analytics.html         # Deep analytics (Analyst/Admin)
│       ├── profile.html           # User settings
│       └── users.html             # User management (Admin only)
│
├── seed.py                        # Populates demo data (60 transactions)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL running locally (or via Docker)

### 1. Clone & set up environment

```bash
git clone https://github.com/yourusername/finance-fix.git
cd finance-fix

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/finance_db
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Create the PostgreSQL database

```sql
-- In psql or pgAdmin
CREATE DATABASE finance_db;
```

### 5. Start the server

```bash
python -m uvicorn app.main:app --reload
```

Tables are auto-created on startup. You should see:

```
INFO:     Application startup complete.
```

### 6. Seed demo data

```bash
python seed.py
```

```
✅ Seed complete!
Admin   → username: admin    password: admin123
Analyst → username: analyst  password: analyst123
Viewer  → username: viewer   password: viewer123
```

### 7. Open the app

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/frontend/pages/login.html` | 🖥️ Frontend Dashboard |
| `http://127.0.0.1:8000/docs` | 📖 Swagger / OpenAPI UI |
| `http://127.0.0.1:8000` | ✅ Health Check |

---

## 🎭 Demo Credentials

<div align="center">

| Role | Username | Password | Access Level |
|:----:|:--------:|:--------:|:-------------|
| 🔴 **Admin** | `admin` | `admin123` | Full CRUD · User management · All analytics |
| 🟡 **Analyst** | `analyst` | `analyst123` | View + filters + analytics · No write access |
| 🟢 **Viewer** | `viewer` | `viewer123` | Read-only · Summaries only |

</div>

> **💡 Tip:** Seed data (60 transactions + 5 budgets) is attached to the **admin** account. Log in as admin to see charts and analytics fully populated.

---

## 📮 API Documentation

Interactive Swagger UI: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**  
Postman Collection: **[View Online](https://documenter.getpostman.com/view/53769985/2sBXiqEoRf)**

### 🔑 Authentication

| Method | Endpoint | Description |
|:------:|:---------|:------------|
| `POST` | `/auth/register` | Create a new account |
| `POST` | `/auth/login` | Login → returns JWT token |

### 💳 Transactions

| Method | Endpoint | Access | Description |
|:------:|:---------|:------:|:------------|
| `GET` | `/transactions` | All roles | List with filters + pagination |
| `POST` | `/transactions` | Admin | Create transaction |
| `GET` | `/transactions/{id}` | All roles | Get single transaction |
| `PUT` | `/transactions/{id}` | Admin | Update transaction |
| `DELETE` | `/transactions/{id}` | Admin | Soft delete |

**Available query filters:** `transaction_type` · `category` · `start_date` · `end_date` · `skip` · `limit`

### 📊 Summary & Analytics

| Method | Endpoint | Access | Returns |
|:------:|:---------|:------:|:--------|
| `GET` | `/summary` | All roles | Full combined summary |
| `GET` | `/summary/overview` | All roles | Income · Expenses · Balance · Savings rate |
| `GET` | `/summary/recent?limit=5` | All roles | Recent activity feed |
| `GET` | `/summary/categories` | Analyst · Admin | Expense per category |
| `GET` | `/summary/income-breakdown` | Analyst · Admin | Income per source category |
| `GET` | `/summary/monthly` | Analyst · Admin | Month-by-month totals |
| `GET` | `/summary/current-month` | Analyst · Admin | This month snapshot |
| `GET` | `/summary/top-spending?top_n=5` | Analyst · Admin | Ranked categories with % |

### 💰 Budget

| Method | Endpoint | Description |
|:------:|:---------|:------------|
| `GET` | `/budget` | List all budgets |
| `POST` | `/budget` | Create / upsert budget |
| `PUT` | `/budget/{id}` | Update specific budget |
| `DELETE` | `/budget/{id}` | Delete budget |
| `GET` | `/budget/status` | Spending vs limits this month |

### 👥 Users

| Method | Endpoint | Access | Description |
|:------:|:---------|:------:|:------------|
| `GET` | `/users/me` | All roles | Own profile |
| `PUT` | `/users/me` | All roles | Update own profile |
| `GET` | `/users` | Admin | All users list |
| `PUT` | `/users/{id}` | Admin | Update any user |
| `DELETE` | `/users/{id}` | Admin | Delete user |

---

## 🛡 Role-Based Access Control

Access is enforced at the **API layer** using FastAPI dependency injection — not just hidden in the UI:

```python
# All roles — read access
@router.get("/transactions")
def list_transactions(user = Depends(get_current_user)):
    ...

# Admin only — write access
@router.post("/transactions")
def create(user = Depends(require_role(UserRole.admin))):
    ...

# Analyst + Admin — analytics access
@router.get("/summary/categories")
def categories(user = Depends(require_role(UserRole.analyst, UserRole.admin))):
    ...
```

<div align="center">

| Permission | 👁️ Viewer | 🔍 Analyst | ⚙️ Admin |
|:-----------|:---------:|:---------:|:-------:|
| View transactions | ✅ | ✅ | ✅ |
| View summaries | ✅ | ✅ | ✅ |
| Export CSV | ✅ | ✅ | ✅ |
| Date / category filters | ❌ | ✅ | ✅ |
| Category analytics | ❌ | ✅ | ✅ |
| Monthly trends | ❌ | ✅ | ✅ |
| Top spending insights | ❌ | ✅ | ✅ |
| Add transactions | ❌ | ❌ | ✅ |
| Edit transactions | ❌ | ❌ | ✅ |
| Delete transactions | ❌ | ❌ | ✅ |
| Set / edit budgets | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

</div>

---

## ✅ Features

### Core Requirements

- [x] **Financial Record CRUD** — Create, view, update, soft-delete transactions
- [x] **Filtering** — By type, category, date range with pagination
- [x] **Summary: Total Income** — `GET /summary/overview` → `total_income`
- [x] **Summary: Total Expenses** — `GET /summary/overview` → `total_expenses`
- [x] **Summary: Current Balance** — `GET /summary/overview` → `balance`
- [x] **Summary: Category Breakdown** — `GET /summary/categories`
- [x] **Summary: Monthly Totals** — `GET /summary/monthly`
- [x] **Summary: Recent Activity** — `GET /summary/recent`
- [x] **Role-Based Access** — Viewer / Analyst / Admin enforced on every route
- [x] **JWT Authentication** — Secure stateless login with bcrypt hashing
- [x] **Input Validation** — Pydantic v2 schemas with custom validators
- [x] **Error Handling** — Proper HTTP status codes and descriptive error messages
- [x] **PostgreSQL Persistence** — Relational DB with indexes and foreign keys
- [x] **API Documentation** — Auto-generated Swagger UI at `/docs`

### Bonus Features

- [x] **Soft Delete** — Transactions flagged `is_deleted=True`, never permanently lost
- [x] **Budget Tracking** — Set limits per category, track live spending vs. limit
- [x] **Pagination** — Skip/limit with total count on all list endpoints
- [x] **CSV Export** — Download transactions or summary from the frontend
- [x] **Seed Script** — One command to populate 60 realistic transactions over 6 months
- [x] **Frontend Dashboard** — Charts, tables, filters fully wired to backend
- [x] **Income Breakdown** — Category-wise income analysis (bonus endpoint)
- [x] **Current Month Snapshot** — Real-time this-month financial summary
- [x] **User Management UI** — Admin can create, update roles, delete users
- [x] **Analytics Page** — Auto-generated financial insights with Chart.js

---

## 🖥 Frontend Pages

| Page | Route | Access |
|------|-------|--------|
| 🔐 Login | `/pages/login.html` | Public |
| 📝 Register | `/pages/register.html` | Public |
| 📊 Dashboard | `/pages/dashboard.html` | All roles |
| 💳 Transactions | `/pages/transaction.html` | All roles (CRUD: Admin only) |
| 💰 Budget | `/pages/budget.html` | All roles (edit: Admin only) |
| 📋 Summary | `/pages/summary.html` | All roles (full analytics: Analyst+Admin) |
| 📈 Analytics | `/pages/analytics.html` | Analyst + Admin |
| 👤 Profile | `/pages/profile.html` | All roles |
| 👥 Users | `/pages/users.html` | Admin only |

---

## 🗄 Database Schema

```sql
-- Users
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR UNIQUE NOT NULL,
    email       VARCHAR UNIQUE NOT NULL,
    full_name   VARCHAR,
    hashed_password VARCHAR NOT NULL,
    role        VARCHAR DEFAULT 'viewer',   -- viewer | analyst | admin
    created_at  TIMESTAMP DEFAULT now()
);

-- Transactions
CREATE TABLE transactions (
    id          SERIAL PRIMARY KEY,
    amount      NUMERIC(12, 2) NOT NULL,
    type        VARCHAR NOT NULL,           -- income | expense
    category    VARCHAR NOT NULL,
    date        DATE NOT NULL,
    notes       TEXT,
    is_deleted  BOOLEAN DEFAULT FALSE,      -- soft delete
    created_at  TIMESTAMP DEFAULT now(),
    updated_at  TIMESTAMP DEFAULT now(),
    user_id     INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Budgets
CREATE TABLE budgets (
    id          SERIAL PRIMARY KEY,
    category    VARCHAR NOT NULL,
    amount      NUMERIC(12, 2) NOT NULL,
    period      VARCHAR DEFAULT 'monthly',
    notes       TEXT,
    created_at  TIMESTAMP DEFAULT now(),
    user_id     INTEGER REFERENCES users(id) ON DELETE CASCADE
);
```

**Relationships:** Each user owns their transactions and budgets. Soft delete via `is_deleted` flag. Budget upsert — creating a budget for an existing category updates it instead of duplicating.

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | PostgreSQL connection string |
| `SECRET_KEY` | `fallback-secret` | JWT signing key (**change in prod!**) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token lifetime in minutes |

---

## 📐 Assumptions

1. **Username + email** are both required for registration; username is used for login
2. **Soft delete** — transactions are flagged `is_deleted=True`, not physically removed
3. **Per-user data isolation** — each user's transactions and budgets are completely separate
4. **Budget upsert** — creating a budget for an existing category updates it rather than duplicating
5. **Seed data linked to admin** — all 60 demo transactions belong to the admin user
6. **Analyst cannot CUD** — analyst is view + filter + insights only, per spec
7. **Category stored as string** — flexible; frontend provides standard dropdown options
8. **JWT expiry 30 minutes** — configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`

---

## 🧪 Testing Guide

### Option 1 — Frontend (Recommended)

```bash
# 1. Start the server
python -m uvicorn app.main:app --reload

# 2. Seed demo data
python seed.py

# 3. Open the app
# http://127.0.0.1:8000/frontend/pages/login.html

# 4. Log in as admin / analyst / viewer to observe role differences
```

### Option 2 — Swagger UI

```
1. Open: http://127.0.0.1:8000/docs
2. POST /auth/login  →  username: admin, password: admin123
3. Copy access_token → click Authorize → paste "Bearer <token>"
4. Test any endpoint
```

### Option 3 — curl

```bash
# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -d "username=admin&password=admin123"

# Store token
TOKEN="your_token_here"

# Full summary
curl http://127.0.0.1:8000/summary \
  -H "Authorization: Bearer $TOKEN"

# Create transaction (admin only)
curl -X POST http://127.0.0.1:8000/transactions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":5000,"type":"income","category":"Salary","date":"2026-04-06","notes":"Monthly salary"}'

# Test role restriction — analyst cannot delete
curl -X DELETE http://127.0.0.1:8000/transactions/1 \
  -H "Authorization: Bearer $ANALYST_TOKEN"
# → Expected: 403 Forbidden
```

---

## 🔮 Known Limitations & Future Improvements

### Current Limitations

- JWT tokens are not server-side revocable (30-min expiry mitigates this)
- Frontend served statically via FastAPI; production would use a CDN
- No email verification on registration

### Planned Improvements

- [ ] Refresh token support with token rotation
- [ ] WebSocket-based real-time dashboard updates
- [ ] Rate limiting on `/auth` endpoints
- [ ] Docker Compose for one-command deployment
- [ ] Unit + integration test suite (pytest)
- [ ] Multi-currency support
- [ ] Email notifications for budget limit breaches

---

## 📦 Requirements

```
fastapi>=0.100.0
uvicorn[standard]
sqlalchemy>=2.0.0
psycopg2-binary
python-jose[cryptography]
passlib[bcrypt]
bcrypt==4.0.1
python-dotenv
pydantic[email]>=2.0.0
python-multipart
```

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1a1a3e,100:0f0f23&height=120&section=footer" width="100%"/>

**Built with by [Mohit Gautam]

*Python Developer Intern Assignment — Zorvyn FinTech Pvt. Ltd. · 2026*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/yourusername)

⭐ If you found this useful, consider giving it a star!

</div>
