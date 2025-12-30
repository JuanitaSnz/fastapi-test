"""add_initial_user

Revision ID: 5a025f5b928c
Revises: e6672e5da324
Create Date: 2025-12-30 12:12:13.475854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a025f5b928c'
down_revision: Union[str, Sequence[str], None] = 'e6672e5da324'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Hash de "admin123" con bcrypt
    hashed_password = '$2b$12$U3qPZoPBep0.ivlaLs.yJOrsmjieLftvJb/7EiSsUVNDdCaGn1tiK'
    
    op.execute(f"""
        INSERT INTO users (email, hashed_password, created_at)
        VALUES ('admin@test.com', '{hashed_password}', NOW())
        ON CONFLICT (email) DO NOTHING;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM users WHERE email = 'admin@test.com';")
