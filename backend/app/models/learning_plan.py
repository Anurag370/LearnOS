from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.learning_goal import LearningGoal
    from app.models.course import Lesson

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LearningPlan(Base):
    __tablename__ = "learning_plans"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    learning_goal_id: Mapped[int] = mapped_column(
        ForeignKey("learning_goals.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ACTIVE",
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

    goal: Mapped["LearningGoal"] = relationship(
        back_populates="learning_plan",
    )

    items: Mapped[list["LearningPlanItem"]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan",
        order_by="LearningPlanItem.position",
    )

class LearningPlanItem(Base):
    __tablename__ = "learning_plan_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("learning_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    position: Mapped[int] = mapped_column(
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PENDING",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    plan: Mapped["LearningPlan"] = relationship(
        back_populates="items",
    )

    lesson: Mapped["Lesson"] = relationship()