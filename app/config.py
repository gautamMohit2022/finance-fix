import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Prateek%4098@localhost:5432/finance_db"
)
SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-change-in-production")

# HS256 = HMAC with SHA-256. It signs the JWT token so nobody can tamper with it.
# The server creates the token, signs it with SECRET_KEY, and verifies the same key on every request.
ALGORITHM: str = "HS256"

# FIX: was 2 minutes — way too short, users would be logged out constantly
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
