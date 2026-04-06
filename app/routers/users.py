from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.dependencies import require_role, AdminOnly, AdminOrAnalyst
from app.auth.password import hash_password
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


# ================= REGISTER =================
@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = AdminOnly  # ✅ ONLY ADMIN CAN CREATE USERS
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role=data.role or UserRole.viewer,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ================= CURRENT USER =================
@router.get("/me", response_model=UserResponse)
def my_profile(current_user: User = Depends(get_current_user)):
    return current_user


# ================= UPDATE OWN PROFILE =================
@router.put("/me", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.username and data.username != current_user.username:
        if db.query(User).filter(User.username == data.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = data.username

    if data.email and data.email != current_user.email:
        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = data.email

    if data.full_name is not None:
        current_user.full_name = data.full_name

    # ❌ VERY IMPORTANT: user cannot change own role
    # if data.role is not None:
    #     current_user.role = data.role

    db.commit()
    db.refresh(current_user)
    return current_user


# ================= GET ALL USERS =================
@router.get("/", response_model=list[UserResponse])
def all_users(
    db: Session = Depends(get_db),
    current_user: User = AdminOrAnalyst  # ✅ ADMIN + ANALYST
):
    return db.query(User).order_by(User.created_at.desc()).all()


# ================= GET USER BY ID =================
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = AdminOnly  # ✅ ADMIN ONLY
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ================= UPDATE USER =================
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = AdminOnly  # ✅ ADMIN ONLY
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.role:
        user.role = data.role

    if data.username:
        user.username = data.username

    if data.email:
        user.email = data.email

    if data.full_name:
        user.full_name = data.full_name

    db.commit()
    db.refresh(user)
    return user


# ================= DELETE USER =================
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = AdminOnly  # ✅ ADMIN ONLY
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": f"User {user_id} deleted successfully"}