from datetime import datetime
from datetime import timezone

from google.oauth2.credentials import Credentials

from app.models.google_account import GoogleAccount
from app.repositories.google_repository import GoogleRepository


class GoogleService:

    def __init__(
        self,
        repository: GoogleRepository,
    ):
        self.repository = repository

    def save_google_account(
        self,
        user_id: int,
        profile: dict,
        credentials: Credentials,
    ) -> GoogleAccount:

        account = self.repository.get_by_user_id(user_id)

        #
        # Create new Google account
        #
        if account is None:

            account = GoogleAccount(
                user_id=user_id,
                google_email=profile["email"],
                google_user_id=profile["id"],
                access_token="",
                refresh_token="",
                token_expiry=datetime.now(timezone.utc),
            )

        #
        # Update latest Google information
        #
        account.google_email = profile["email"]
        account.google_user_id = profile["id"]

        #
        # Access token
        #
        account.access_token = credentials.token

        #
        # Google only returns a refresh token the first time
        # the user grants offline access.
        #
        if credentials.refresh_token:
            account.refresh_token = credentials.refresh_token

        #
        # Token expiration
        #
        if credentials.expiry:
            account.token_expiry = credentials.expiry

        #
        # Insert
        #
        if account.id is None:
            return self.repository.create(account)

        #
        # Update
        #
        self.repository.update()

        return account
