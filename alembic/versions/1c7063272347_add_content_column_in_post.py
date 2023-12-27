"""add content column in post

Revision ID: 1c7063272347
Revises: 11728f7096f1
Create Date: 2023-12-28 06:57:37.843422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c7063272347'
down_revision: Union[str, None] = '11728f7096f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('rating', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'created_at')
    pass
