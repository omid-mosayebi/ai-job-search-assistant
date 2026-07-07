from sqlalchemy.orm import Session

from app.models.email import Email


class EmailRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, email: Email):
        self.db.add(email)
        self.db.commit()
        self.db.refresh(email)
        return email

    def update(self):
        self.db.commit()

    def get(self, email_id: int):
        return (
            self.db.query(Email)
            .filter(Email.id == email_id)
            .first()
        )

    def get_by_gmail_id(self, gmail_id: str):
        return (
            self.db.query(Email)
            .filter(Email.gmail_id == gmail_id)
            .first()
        )

    def get_by_user(self, user_id: int):
        return (
            self.db.query(Email)
            .filter(Email.user_id == user_id)
            .order_by(Email.sent_at.desc())
            .all()
        )

    def get_job_related(self, user_id: int):
        return (
            self.db.query(Email)
            .filter(
                Email.user_id == user_id,
                Email.is_job_related.is_(True),
            )
            .order_by(Email.sent_at.desc())
            .all()
        )

    def delete(self, email: Email):
        self.db.delete(email)
        self.db.commit()
