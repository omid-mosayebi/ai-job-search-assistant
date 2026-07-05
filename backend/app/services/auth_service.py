from fastapi import HTTPException
from fastapi import status

from app.core.security import create_access_token
from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(
        self,
        email: str,
        password: str,
    ):

        user = self.repository.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }
