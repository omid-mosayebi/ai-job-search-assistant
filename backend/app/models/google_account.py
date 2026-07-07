from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class GoogleAccount(Base):

    __tablename__ = "google_accounts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    google_email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    google_user_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    access_token: Mapped[str] = mapped_column(
        String(2048),
    )

    refresh_token: Mapped[str] = mapped_column(
        String(2048),
    )

    token_expiry: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship(
    "User",
    back_populates="google_accounts",
)
