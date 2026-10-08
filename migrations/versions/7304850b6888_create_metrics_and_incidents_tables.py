"""create metrics and incidents tables

Revision ID: 7304850b6888
Revises: 
Create Date: 2026-10-08 22:39:04.841964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7304850b6888'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE metrics (
            id SERIAL PRIMARY KEY,
            service TEXT NOT NULL,
            latency_ms DOUBLE PRECISION NOT NULL,
            error_rate DOUBLE PRECISION NOT NULL,
            recorded_at TIMESTAMPTZ NOT NULL
        )
    """)

    op.execute("""

    CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    service TEXT NOT NULL,
    latency_ms DOUBLE PRECISION NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    detected_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
""")

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE incidents")
    op.execute("DROP TABLE metrics")
