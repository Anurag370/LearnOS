from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.learning_plan import LearningPlan
    
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LearningGoal(Base):
    __tablename__ = "learning_goals"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    desired_outcome: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="ACTIVE")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    learning_plan: Mapped["LearningPlan | None"] = relationship(
    back_populates="goal",
    uselist=False,
    cascade="all, delete-orphan",
)