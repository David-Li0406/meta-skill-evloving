"""add_titulo_ml_to_productos_erp

Example Alembic migration following Pricing App patterns.
Shows: descriptive name, proper up/down, indexes.

Revision ID: 5cf5f4b6e839
Revises: abc123def456
Create Date: 2025-01-15 10:30:00.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5cf5f4b6e839'
down_revision = 'abc123def456'
branch_labels = None
depends_on = None

def upgrade():
    """
    Add titulo_ml column to productos_erp table.
    This field stores the MercadoLibre listing title for sync purposes.
    """
    # Add column
    op.add_column(
        'productos_erp',
        sa.Column('titulo_ml', sa.String(255), nullable=True, comment='MercadoLibre listing title')
    )
    
    # Add index for performance (ML sync queries filter by this)
    op.create_index(
        'idx_productos_titulo_ml',
        'productos_erp',
        ['titulo_ml'],
        unique=False
    )

def downgrade():
    """
    Remove titulo_ml column and its index.
    """
    # Drop index first (required before dropping column)
    op.drop_index('idx_productos_titulo_ml', table_name='productos_erp')
    
    # Drop column
    op.drop_column('productos_erp', 'titulo_ml')
