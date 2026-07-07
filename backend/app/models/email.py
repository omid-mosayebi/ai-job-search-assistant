from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class Email(Base):

    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    #
    # Owner
    #
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    #
    # Gmail identifiers
    #
    gmail_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )

    thread_id: Mapped[str] = mapped_column(
        String(128),
        index=True,
    )

    #
    # Basic email fields
    #
    subject: Mapped[str | None] = mapped_column(
        String(1000),
    )

    sender_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    sender_email: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
    )

    recipient: Mapped[str | None] = mapped_column(
        String(500),
    )

    sent_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
    )

    snippet: Mapped[str | None] = mapped_column(
        Text,
    )

    body: Mapped[str | None] = mapped_column(
        Text,
    )

    #
    # Classification
    #
    is_job_related: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
    )

    confidence: Mapped[int | None] = mapped_column(
        Integer,
    )

    #
    # AI extracted fields
    #
    company: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
    )

    position: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
    )

    recruiter_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    recruiter_email: Mapped[str | None] = mapped_column(
        String(255),
    )

    application_status: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
    )

    interview_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
    )

    #
    # AI summary
    #
    summary: Mapped[str | None] = mapped_column(
        Text,
    )

    #
    # Processing
    #
    processed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True,
    )

    ai_processed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True,
    )

    #
    # Audit
    #
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    #
    # Relationships
    #
    user = relationship(
        "User",
        back_populates="emails",
    )
