from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.jwt_handler import decode_access_token
from app.database import get_db
from app.models.user import User, UserRole


# ================= AUTH SCHEME =================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ================= GET CURRENT USER =================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Extract user from JWT token.
    Used in all protected routes.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    username: str = payload.get("sub")
    if not username:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception

    return user


# ================= ROLE-BASED ACCESS =================
def require_role(*roles: UserRole):
    """
    Reusable role-based dependency.

    Example:
        Depends(require_role(UserRole.admin))
        Depends(require_role(UserRole.admin, UserRole.analyst))
    """
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in roles]}",
            )
        return current_user

    return checker


# ================= SHORTCUT DEPENDENCIES =================

# 🔥 Use these directly in routes (clean code)

# Only admin
AdminOnly = Depends(require_role(UserRole.admin))

# Admin + Analyst (read access)
AdminOrAnalyst = Depends(require_role(UserRole.admin, UserRole.analyst))

# Any logged-in user (viewer + others)
AnyUser = Depends(get_current_user)