from .base import Base
from sqlalchemy import Column, Integer, String


class SubCategory(Base):
    __tablename__ = 'sub_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)