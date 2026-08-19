from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base

# Import models so SQLAlchemy knows about them
from app import models

from app.routers.applicant import (
    router as applicant_router
)

from app.routers.debug import (
    router as debug_router
)

from app.routers.auth import (
    router as auth_router
)

from app.routers.loan import (
    router as loan_router
)

from app.routers.lender import (
    router as lender_router
)

# Ensure all database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Credit Risk Assessment API",
    description="Backend for Credit Rating and Loan Risk Assessment",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

app.include_router(
    auth_router
)

app.include_router(
    debug_router
)

app.include_router(
    applicant_router
)

app.include_router(
    loan_router
)

app.include_router(
    lender_router
)

@app.get("/")
def root():

    return {
        "message":
            "Credit Risk Assessment API is running"
    }


@app.get("/health")
def health_check():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }