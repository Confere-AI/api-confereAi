"""create initial tables

Revision ID: 0001_create_initial_tables
Revises:
Create Date: 2025-11-16
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_create_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create engajamento_documento first (others reference it)
    op.create_table(
        'engajamento_documento',
        sa.Column('id_engajamento', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('documento_id', sa.Integer(), nullable=True),
        sa.Column('visualizacoes', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('curtidas', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('probabilidade_compartilhamento', sa.Float(), nullable=True),
        sa.Column('tempo_medio', sa.Float(), nullable=True),
        sa.Column('id_relatorio', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    op.create_table(
        'captura_frame',
        sa.Column('id_frame', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('documento_id', sa.Integer(), nullable=True),
        sa.Column('frame_index', sa.Integer(), nullable=False),
        sa.Column('timestamp_ms', sa.Integer(), nullable=True),
        sa.Column('path', sa.String(length=512), nullable=True),
        sa.Column('faces_count', sa.Integer(), nullable=True),
        sa.Column('mean_confidence', sa.Float(), nullable=True),
        sa.Column('id_engajamento', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    op.create_table(
        'expressoes_corporal',
        sa.Column('id_expressao_c', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('intensidade', sa.Float(), nullable=True),
        sa.Column('frequencia', sa.Integer(), nullable=True),
        sa.Column('id_engajamento', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    op.create_table(
        'expressoes_faciais',
        sa.Column('id_expressao_f', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('intensidade', sa.Float(), nullable=True),
        sa.Column('frequencia', sa.Integer(), nullable=True),
        sa.Column('id_engajamento', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    # Add ForeignKey constraints after tables are created
    op.create_foreign_key(
        'fk_expressoes_corporal_engajamento', 'expressoes_corporal', 'engajamento_documento', ['id_engajamento'], ['id_engajamento'], ondelete='SET NULL'
    )
    op.create_foreign_key(
        'fk_expressoes_faciais_engajamento', 'expressoes_faciais', 'engajamento_documento', ['id_engajamento'], ['id_engajamento'], ondelete='SET NULL'
    )
    op.create_foreign_key(
        'fk_captura_frame_engajamento', 'captura_frame', 'engajamento_documento', ['id_engajamento'], ['id_engajamento'], ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('fk_captura_frame_engajamento', 'captura_frame', type_='foreignkey')
    op.drop_constraint('fk_expressoes_faciais_engajamento', 'expressoes_faciais', type_='foreignkey')
    op.drop_constraint('fk_expressoes_corporal_engajamento', 'expressoes_corporal', type_='foreignkey')

    op.drop_table('expressoes_faciais')
    op.drop_table('expressoes_corporal')
    op.drop_table('captura_frame')
    op.drop_table('engajamento_documento')
