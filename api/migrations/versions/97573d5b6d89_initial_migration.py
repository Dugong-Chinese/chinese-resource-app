"""Initial migration.

Revision ID: 97573d5b6d89
Revises: 
Create Date: 2020-08-10 19:12:17.513207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "97573d5b6d89"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "resource",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "date_added",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["resource.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("value"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "date_joined",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("salt", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "resource_name",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["resource_id"], ["resource.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("value"),
    )
    op.create_table(
        "resource_url",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["resource_id"], ["resource.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("value"),
    )
    op.create_table(
        "tags_to_resources_mtm",
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["resource_id"], ["resource.id"]),
        sa.ForeignKeyConstraint(["tag_id"], ["tag.id"]),
        sa.PrimaryKeyConstraint("tag_id", "resource_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tags_to_resources_mtm")
    op.drop_table("resource_url")
    op.drop_table("resource_name")
    op.drop_table("user")
    op.drop_table("tag")
    op.drop_table("resource")
    # ### end Alembic commands ###