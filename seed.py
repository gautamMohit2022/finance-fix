"""
seed.py — Populates the database with demo data for testing.
Run with:  python seed.py
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from datetime import date, timedelta
import random
from app.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.transaction import Transaction, TransactionType
from app.models.budget import Budget
from app.auth.password import hash_password

Base.metadata.create_all(bind=engine)

CATEGORIES_EXPENSE = ["Food", "Rent", "Travel", "Shopping", "Health", "Utilities", "Entertainment"]
CATEGORIES_INCOME  = ["Salary", "Freelance", "Investment", "Other"]

def seed():
    db = SessionLocal()
    try:
        # ── Clear existing data ────────────────────────────────
        print("🗑️  Clearing old seed data...")
        db.query(Transaction).delete()
        db.query(Budget).delete()
        db.query(User).filter(User.username.in_(["admin", "analyst", "viewer"])).delete()
        db.commit()

        # ── Create 3 demo users (one per role) ────────────────
        print("👤 Creating demo users...")
        users = [
            User(username="admin",   email="admin@fintrack.com",   full_name="Admin User",
                 hashed_password=hash_password("admin123"),   role=UserRole.admin),
            User(username="analyst", email="analyst@fintrack.com", full_name="Analyst User",
                 hashed_password=hash_password("analyst123"), role=UserRole.analyst),
            User(username="viewer",  email="viewer@fintrack.com",  full_name="Viewer User",
                 hashed_password=hash_password("viewer123"),  role=UserRole.viewer),
        ]
        db.add_all(users)
        db.commit()
        for u in users:
            db.refresh(u)

        admin = users[0]

        # ── Create transactions (6 months of data) ────────────
        print("💳 Creating 60 transactions...")
        txns = []
        for i in range(60):
            d = date.today() - timedelta(days=random.randint(0, 180))
            is_income = random.random() < 0.25
            txns.append(Transaction(
                amount   = round(random.uniform(500, 50000), 2) if is_income else round(random.uniform(100, 8000), 2),
                type     = TransactionType.income if is_income else TransactionType.expense,
                category = random.choice(CATEGORIES_INCOME if is_income else CATEGORIES_EXPENSE),
                date     = d,
                notes    = f"Demo transaction #{i+1}",
                user_id  = admin.id,
            ))
        db.add_all(txns)
        db.commit()

        # ── Create budgets ─────────────────────────────────────
        print("🎯 Creating budgets...")
        budgets = [
            Budget(category="Food",          amount=8000,  period="monthly", user_id=admin.id),
            Budget(category="Rent",          amount=15000, period="monthly", user_id=admin.id),
            Budget(category="Travel",        amount=5000,  period="monthly", user_id=admin.id),
            Budget(category="Shopping",      amount=4000,  period="monthly", user_id=admin.id),
            Budget(category="Entertainment", amount=2000,  period="monthly", user_id=admin.id),
        ]
        db.add_all(budgets)
        db.commit()

        print("\n✅ Seed complete!")
        print("─" * 40)
        print("Demo login credentials:")
        print("  Admin   → username: admin    password: admin123")
        print("  Analyst → username: analyst  password: analyst123")
        print("  Viewer  → username: viewer   password: viewer123")
        print("─" * 40)

    except Exception as e:
        print(f"❌ Seed failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
