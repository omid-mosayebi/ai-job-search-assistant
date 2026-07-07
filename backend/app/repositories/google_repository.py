from sqlalchemy.orm import Session

from app.models.google_account import GoogleAccount


class GoogleRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        account: GoogleAccount,
    ) -> GoogleAccount:

        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

        return account

    def update(self):

        self.db.commit()

    def get_by_id(
        self,
        account_id: int,
    ) -> GoogleAccount | None:

        return (
            self.db.query(GoogleAccount)
            .filter(GoogleAccount.id == account_id)
            .first()
        )

    def get_by_user_id(
        self,
        user_id: int,
    ) -> GoogleAccount | None:

        return (
            self.db.query(GoogleAccount)
            .filter(GoogleAccount.user_id == user_id)
            .first()
        )

    def get_by_google_email(
        self,
        email: str,
    ) -> GoogleAccount | None:

        return (
            self.db.query(GoogleAccount)
            .filter(GoogleAccount.google_email == email)
            .first()
        )

    def get_by_google_user_id(
        self,
        google_user_id: str,
    ) -> GoogleAccount | None:

        return (
            self.db.query(GoogleAccount)
            .filter(
                GoogleAccount.google_user_id == google_user_id
            )
            .first()
        )

    def delete(
        self,
        account: GoogleAccount,
    ):

        self.db.delete(account)
        self.db.commit()
