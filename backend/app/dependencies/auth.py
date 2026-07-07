from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError
from jose import jwt

from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY
from app.core.security import ALGORITHM

from app.dependencies.database import get_database

from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_database),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = int(payload.get("sub"))

    except JWTError:

        raise credentials_exception

    repository = UserRepository(db)

    user = repository.get(user_id)

    if user is None:
        raise credentials_exception

    return user
