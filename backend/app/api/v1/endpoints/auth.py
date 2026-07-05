from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_database
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_database),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    return service.login(
        request.email,
        request.password,
    )
