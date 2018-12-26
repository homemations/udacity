"""
    Project Name: Catalog App
    File: Models (Database)
    Author: Stephen Harris
    Created Date:  12/18/2018
"""

# Import required libraries for db framework
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Get the base class mapper from SQLalchemy
Base = declarative_base()

"""
    Model: User
    Attributes:
        id: User ID  table primary key.
        name: User full name, 128 character max length.
        email: User email address, 256 character max length.
"""
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), nullable=False)

"""
    Model:  Category
    Attributes:
        id: Category ID table primary key.
        name: Category name, 128 character max length.
        items: Relationship of Items to category.
"""
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    items = relationship('Item', cascade="save-update, merge, delete")

    # Returns serialized category only data
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name
        }

    # Returns serialized category & Item(s) data
    @property
    def categoriesItemsSerialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'item' : [i.serialize for i in self.items]
        }

"""
    Model:  Item
    Attributes:
        id: Item ID table primary key.
        name:  Item name, 128 character max length.
        description: Item description.
        quantity: Number of items.
        categoryID: Category ID foriegn key relationship to category.
        userID: User ID foriegn key relationship to User.
"""
class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String)

    # Category Foreign key and model relationship
    categoryID = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    # User Foreign key and model relationship
    userID = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Returns serialized item data.
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'categoryID' : self.categoryID,
            'name' : self.name,
            'description' : self.description
        }

# Create empty database and tables.
def createDB(dburi):
    engine = create_engine(dburi)
    Base.metadata.create_all(engine)
