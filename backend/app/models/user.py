from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment

from datetime import datetime

from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="STUDENT",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student_profile: Mapped["StudentProfile | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    current_skill_level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    available_study_minutes: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="student_profile",
    )