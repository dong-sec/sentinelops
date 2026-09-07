from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    event_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=True,
    )

    policy_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("policies.id"),
        nullable=True,
    )

    initiated_by: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    response_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    target_ip: Mapped[str | None] = mapped_column(
        INET,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="PENDING",
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    steps = relationship(
        "ResponseStep",
        back_populates="response",
        cascade="all, delete-orphan",
        order_by="ResponseStep.step_order",
    )


class ResponseStep(Base):
    __tablename__ = "response_steps"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    response_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("responses.id", ondelete="CASCADE"),
        nullable=False,
    )

    step_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    step_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    metadata_: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    response = relationship(
        "Response",
        back_populates="steps",
    )