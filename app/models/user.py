import enum
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(str, enum.Enum):
    viewer  = "viewer"   # Read-only: view transactions and summaries
    analyst = "analyst"  # Read + filters + detailed analytics
    admin   = "admin"    # Full access: CRUD + user management


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50),  unique=True, index=True, nullable=False)
    email           = Column(String(120), unique=True, index=True, nullable=False)
    full_name       = Column(String(100), nullable=True)   # FIX: added — frontend sends this on register
    hashed_password = Column(String(255), nullable=False)
    role            = Column(Enum(UserRole), default=UserRole.viewer, nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow, nullable=False)

    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan")
    budgets      = relationship("Budget",      back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"
