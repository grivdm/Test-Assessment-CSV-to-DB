from .base import Base
from sqlalchemy import Column, Integer, ForeignKey

class FoodItemSubcategory(Base):
    __tablename__ = 'food_item_subcategory'

    id = Column(Integer, primary_key=True)
    food_item_id = Column(Integer, ForeignKey('food_items.id'))
    subcategory_id = Column(Integer, ForeignKey('sub_categories.id'))

    