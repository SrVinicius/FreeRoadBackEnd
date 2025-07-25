"""New revision

Revision ID: d72149f16e50
Revises: 
Create Date: 2025-07-19 13:01:29.506758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd72149f16e50'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('weeks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('km_atual', sa.Numeric(precision=10, scale=2), nullable=False, comment='Quilometragem atual do veículo'),
    sa.Column('km_final', sa.Numeric(precision=10, scale=2), nullable=False, comment='Quilometragem final do veículo'),
    sa.Column('custo', sa.Numeric(precision=10, scale=2), nullable=False, comment='Custo total do abastecimento'),
    sa.Column('eficiencia', sa.Numeric(precision=5, scale=2), nullable=True, comment='Eficiência em km/l'),
    sa.Column('litros_abastecidos', sa.Numeric(precision=8, scale=3), nullable=False, comment='Quantidade de litros abastecidos'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weeks')
    op.drop_table('users')
    # ### end Alembic commands ###
