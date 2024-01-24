from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()


cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()


# items = session.query(MenuItem).all()
# for item in items:
# ...     print (item.name)

# veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
# for veggieBurger in veggieBurgers:
#     print (veggieBurger.id)
#     print (veggieBurger.price)
#     print (veggieBurger.restaurant.name)
#     print ("\n")


# to update price of urbanveggieburger
# veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
# UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 4).one()
# UrbanVeggieBurger.price = '$2.99'
# session.add(UrbanVeggieBurger)
# session.commit()


# to update price of all veggieburgers to 2.99
# veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
# for veggieBurger in veggieBurgers:
#     if veggieBurger.price != '$2.99':
#         veggieBurger.price = '$2.99'
#         session.add(veggieBurger)
#         session.commit()


#delete Auntie Ann's Diner
# spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
# print (spinach.restaurant.name)
# printed this -> Auntie Ann's Diner 
# session.delete(spinach)
# session.commit()