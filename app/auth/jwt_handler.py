from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT token.
    data: usually {"sub": username} — "sub" is the JWT standard for subject (who owns the token)
    expires_delta: how long until the token is invalid
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # "exp" is a standard JWT claim meaning expiry time.
    # When we decode the token later, jose automatically checks this and rejects expired tokens.
    to_encode.update({"exp": expire})

    # jwt.encode() creates the signed token string: header.payload.signature
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes and validates a JWT token.
    Returns the payload dict if valid, None if expired or tampered.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
