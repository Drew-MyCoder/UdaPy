import os
import sys # useful for manipulating different runtime environment
 
from sqlalchemy import Column, ForeignKey, Integer, String # useful for our mapper code

from sqlalchemy.ext.declarative import declarative_base # for configuration and class code

from sqlalchemy.orm import relationship # create foreign key relationships

from sqlalchemy import create_engine # useful in configuration code at the end of the file

Base = declarative_base() # alerts that our class is special sqlalchemy class



class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key= True
    )


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column (
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key=True
    )
    course = Column(
        String(250)
    )
    description = Column(
        String(250)
    )
    price = Column(String(8))
    restaurant_id = Column(
        Integer, ForeignKey('restaurant.id')
    )
    restaurant = relationship(Restaurant)



# end of file, points to database we'll use
engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.create_all(engine) # adds classes that are created as new tables in the database 