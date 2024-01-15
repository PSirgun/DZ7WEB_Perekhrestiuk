"""add table

Revision ID: 4683d1686bf6
Revises: 582fcfaadd6f
Create Date: 2024-01-14 14:10:04.941593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4683d1686bf6'
down_revision: Union[str, None] = '582fcfaadd6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from add_db import init_bd, drop_bd, engine

def upgrade() -> None:
   init_bd(engine)


def downgrade() -> None:
    drop_bd(engine)
