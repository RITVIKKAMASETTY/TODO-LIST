"""create phone number for user column

Revision ID: a59a6db2298f
Revises: 
Create Date: 2025-06-23 18:56:06.163669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a59a6db2298f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=False, server_default='N/A'))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
