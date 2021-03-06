"""empty message

Revision ID: 0abedf03157b
Revises: 8475f7d96e68
Create Date: 2020-08-19 10:49:17.966398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0abedf03157b"
down_revision = "8475f7d96e68"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "api_key",
        sa.Column(
            "creation_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
    )
    op.drop_column("api_key", "date_emitted")
    op.add_column(
        "resource",
        sa.Column(
            "creation_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
    )
    op.drop_column("resource", "date_added")
    op.add_column(
        "review",
        sa.Column(
            "creation_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
    )
    op.drop_column("review", "date_added")
    op.add_column(
        "user",
        sa.Column(
            "creation_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
    )
    op.drop_column("user", "date_joined")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "date_joined",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("user", "creation_date")
    op.add_column(
        "review",
        sa.Column(
            "date_added",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("review", "creation_date")
    op.add_column(
        "resource",
        sa.Column(
            "date_added",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("resource", "creation_date")
    op.add_column(
        "api_key",
        sa.Column(
            "date_emitted",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("api_key", "creation_date")
    # ### end Alembic commands ###
