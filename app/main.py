from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, summary, transactions, users, budget

# Create all DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="💰 Finance Tracking System",
    description="Python Finance Backend — FastAPI + PostgreSQL",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allows the frontend (opened as a file or on localhost) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In production, set to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Register all routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(users.router)
app.include_router(budget.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# Global error handler — catches any unhandled exception
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."},
    )



@app.get("/", include_in_schema=False)
def root():
    return {"message": "API is running"}# Root — health check + serve dashboard
"""@app.get("/", tags=["Health"])
def root():
    return {
        "status": "✅ running",
        "project": "Finance Tracking System",
        "version": "2.0.0",
        "docs": "/docs",
    }"""

@app.get("/dashboard", tags=["Frontend"])
def serve_dashboard():
    return FileResponse("frontend/pages/dashboard.html")
