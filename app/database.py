from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

# autocommit=False → changes are NOT saved to DB until you call db.commit()
#   This gives you control: if something fails mid-request, you can rollback cleanly.
# autoflush=False → SQLAlchemy won't auto-sync pending changes to DB before every query.
#   Prevents accidental half-written data from being visible during a transaction.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency injected into every route that needs DB access.
    yield gives the session to the route, finally always closes it — even on errors.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
