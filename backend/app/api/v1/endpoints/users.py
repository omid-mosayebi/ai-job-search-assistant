from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_database
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/")
def get_users(db: Session = Depends(get_database)):
    repository = UserRepository(db)
    service = UserService(repository)

    return service.get_users()


@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_database),
):
    repository = UserRepository(db)
    service = UserService(repository)

    return service.create_user(user)
