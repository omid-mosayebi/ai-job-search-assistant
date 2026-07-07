from fastapi import FastAPI
from app.api.v1.endpoints.google import router as google_router

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["Users"],
)

app.include_router(
    google_router,
    prefix="/api/v1/google",
    tags=["Google"],
)

@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
