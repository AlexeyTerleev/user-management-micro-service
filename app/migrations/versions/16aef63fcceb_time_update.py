"""time_update

Revision ID: 16aef63fcceb
Revises: ba9456c12bf5
Create Date: 2023-10-06 20:06:56.692175

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16aef63fcceb"
down_revision: Union[str, None] = "ba9456c12bf5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "tmp")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("tmp", sa.INTEGER(), autoincrement=False, nullable=False)
    )
    # ### end Alembic commands ###