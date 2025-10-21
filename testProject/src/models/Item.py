# src/models/Item.py

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.config.db_config import Base
from sqlalchemy.dialects.mysql import TEXT

# Association table for many-to-many relationship between Item and User
item_user_association = Table(
    'item_user_association',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class Item(Base):

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    color = Column(String(100), nullable=False)
    image = Column(String(500), nullable=False)
    location = Column(String(15), nullable=False)
    formula = Column(String(30), nullable=False)
    description = Column(TEXT, nullable=False)

    # Relationships
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", backref="items_owned")

    userList = relationship("User", secondary=item_user_association, backref="items_saved")
