from app.models.email import Email
from app.repositories.email_repository import EmailRepository


class EmailService:

    def __init__(self, repository: EmailRepository):
        self.repository = repository

    def save(self, data: dict):

        existing = self.repository.get_by_gmail_id(
            data["gmail_id"]
        )

        if existing:
            return existing

        email = Email(**data)

        return self.repository.create(email)

    def get(self, email_id: int):
        return self.repository.get(email_id)

    def get_user_emails(self, user_id: int):
        return self.repository.get_by_user(user_id)

    def get_job_related(self, user_id: int):
        return self.repository.get_job_related(user_id)
