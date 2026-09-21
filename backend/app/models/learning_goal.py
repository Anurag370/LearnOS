from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LearningGoal(Base):
    __tablename__ = "learning_goals"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"), nullable=False, index=True)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    target_date: Mapped[date] = mapped_column(Date, nullable=False)

    desired_outcome: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[bool] = mapped_column(String(30), nullable=False, default="ACTIVE")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
