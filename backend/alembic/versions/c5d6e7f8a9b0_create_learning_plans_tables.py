"""create learning_plans and learning_plan_items tables

Revision ID: c5d6e7f8a9b0
Revises: b3f4a5c6d7e8
Create Date: 2026-09-21 20:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5d6e7f8a9b0'
down_revision: Union[str, Sequence[str], None] = 'b3f4a5c6d7e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the learning plan tables."""
    op.create_table('learning_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('learning_goal_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=30), server_default='ACTIVE', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['learning_goal_id'], ['learning_goals.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_plans_learning_goal_id'), 'learning_plans', ['learning_goal_id'], unique=True)
    op.create_index(op.f('ix_learning_plans_user_id'), 'learning_plans', ['user_id'], unique=False)

    op.create_table('learning_plan_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=30), server_default='PENDING', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['plan_id'], ['learning_plans.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_plan_items_lesson_id'), 'learning_plan_items', ['lesson_id'], unique=False)
    op.create_index(op.f('ix_learning_plan_items_plan_id'), 'learning_plan_items', ['plan_id'], unique=False)


def downgrade() -> None:
    """Drop the learning plan tables."""
    op.drop_index(op.f('ix_learning_plan_items_plan_id'), table_name='learning_plan_items')
    op.drop_index(op.f('ix_learning_plan_items_lesson_id'), table_name='learning_plan_items')
    op.drop_table('learning_plan_items')
    op.drop_index(op.f('ix_learning_plans_user_id'), table_name='learning_plans')
    op.drop_index(op.f('ix_learning_plans_learning_goal_id'), table_name='learning_plans')
    op.drop_table('learning_plans')