from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
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

    modules: Mapped[list["Module"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.position",
    )

    topics: Mapped[list["Topic"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    position: Mapped[int] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    course: Mapped["Course"] = relationship(
        back_populates="modules",
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Lesson.position",
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    position: Mapped[int] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    module: Mapped["Module"] = relationship(
        back_populates="lessons",
    )

    __table_args__ = (
        UniqueConstraint(
            "module_id",
            "slug",
            name="uq_lesson_module_slug",
        ),
    )


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    course: Mapped["Course"] = relationship(
        back_populates="topics",
    )

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "slug",
            name="uq_topic_course_slug",
        ),
    )

