"""Added initial tables

Revision ID: 66638893491a
Revises: 
Create Date: 2023-06-22 22:31:17.660472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66638893491a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sub_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('food_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=True),
    sa.Column('cal_fat', sa.Integer(), nullable=True),
    sa.Column('total_fat', sa.Integer(), nullable=True),
    sa.Column('sat_fat', sa.Integer(), nullable=True),
    sa.Column('trans_fat', sa.Integer(), nullable=True),
    sa.Column('cholesterol', sa.Integer(), nullable=True),
    sa.Column('sodium', sa.Integer(), nullable=True),
    sa.Column('total_carb', sa.Integer(), nullable=True),
    sa.Column('fiber', sa.Integer(), nullable=True),
    sa.Column('sugar', sa.Integer(), nullable=True),
    sa.Column('protein', sa.Integer(), nullable=True),
    sa.Column('vit_a', sa.Integer(), nullable=True),
    sa.Column('vit_c', sa.Integer(), nullable=True),
    sa.Column('calcium', sa.Integer(), nullable=True),
    sa.Column('salad', sa.String(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('sub_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ),
    sa.ForeignKeyConstraint(['sub_category_id'], ['sub_categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('food_item_subcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('food_item_id', sa.Integer(), nullable=True),
    sa.Column('subcategory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['food_item_id'], ['food_items.id'], ),
    sa.ForeignKeyConstraint(['subcategory_id'], ['sub_categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('food_item_subcategory')
    op.drop_table('food_items')
    op.drop_table('sub_categories')
    op.drop_table('restaurants')
    op.drop_table('categories')
    # ### end Alembic commands ###
