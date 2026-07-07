from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_database

from app.oauth.google import (
    create_authorization,
    exchange_code,
    get_user_info,
)

from app.repositories.google_repository import GoogleRepository
from app.services.google_service import GoogleService

router = APIRouter()


@router.get("/login")
def google_login(
    current_user=Depends(get_current_user),
):

    return RedirectResponse(
        url=create_authorization(current_user.id),
        status_code=302,
    )


@router.get("/callback")
def google_callback(
    request: Request,
    db: Session = Depends(get_database),
):

    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing authorization code.",
        )

    if not state:
        raise HTTPException(
            status_code=400,
            detail="Missing OAuth state.",
        )

    credentials, user_id = exchange_code(
        code=code,
        state=state,
    )

    profile = get_user_info(credentials)

    repository = GoogleRepository(db)
    service = GoogleService(repository)

    account = service.save_google_account(
        user_id=user_id,
        profile=profile,
        credentials=credentials,
    )

    return {
        "message": "Google account connected successfully.",
        "google_email": account.google_email,
        "google_user_id": account.google_user_id,
    }
