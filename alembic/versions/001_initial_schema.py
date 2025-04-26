"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-04-26

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('ui_theme', sa.String(), nullable=True),
        sa.Column('camera_mode', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)

    # Create avatar table
    op.create_table(
        'avatar',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('provider_id', sa.String(), nullable=True),
        sa.Column('behavior_settings', sa.JSON(), nullable=True),
        sa.Column('appearance_settings', sa.JSON(), nullable=True),
        sa.Column('voice_settings', sa.JSON(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_predesigned', sa.Boolean(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_avatar_id'), 'avatar', ['id'], unique=False)
    op.create_index(op.f('ix_avatar_name'), 'avatar', ['name'], unique=False)

    # Create product table
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
    op.create_index(op.f('ix_product_name'), 'product', ['name'], unique=False)

    # Create subscription table
    op.create_table(
        'subscription',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('BASIC', 'PREMIUM', name='subscriptiontype'), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('billing_period', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('payment_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscription_id'), 'subscription', ['id'], unique=False)

    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('avatar_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('conversation_metadata', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['avatar_id'], ['avatar.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversation_id'), 'conversation', ['id'], unique=False)
    op.create_index(op.f('ix_conversation_title'), 'conversation', ['title'], unique=False)

    # Create message table
    op.create_table(
        'message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_user', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('conversation_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_id'), 'message', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_message_id'), table_name='message')
    op.drop_table('message')
    op.drop_index(op.f('ix_conversation_title'), table_name='conversation')
    op.drop_index(op.f('ix_conversation_id'), table_name='conversation')
    op.drop_table('conversation')
    op.drop_index(op.f('ix_subscription_id'), table_name='subscription')
    op.drop_table('subscription')
    op.drop_index(op.f('ix_product_name'), table_name='product')
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_avatar_name'), table_name='avatar')
    op.drop_index(op.f('ix_avatar_id'), table_name='avatar')
    op.drop_table('avatar')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
