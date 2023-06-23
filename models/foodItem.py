from .base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey


# FoodItem model
class FoodItem(Base):
    __tablename__ = 'food_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    calories = Column(Integer)
    cal_fat = Column(Float)
    total_fat = Column(Float)
    sat_fat = Column(Float)
    trans_fat = Column(Float)
    cholesterol = Column(Float)
    sodium = Column(Float)
    total_carb = Column(Float)
    fiber = Column(Float)
    sugar = Column(Float)
    protein = Column(Float)
    vit_a = Column(Float)
    vit_c = Column(Float)
    calcium = Column(Float)
    salad = Column(String)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))