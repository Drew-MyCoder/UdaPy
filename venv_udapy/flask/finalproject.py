from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem


# Fake Restaurants
# restaurant = {"name": "The CRUDdy Crab", "id": "1"}

# restaurants = [
#     {"name": "The CRUDdy Crab", "id": "1"},
#     {"name": "Blue Burgers", "id": "2"},
#     {"name": "Taco Hut", "id": "3"},
# ]


# # Fake Menu Items
# items = [
#     {
#         "name": "Cheese Pizza",
#         "description": "made with fresh cheese",
#         "price": "$5.99",
#         "course": "Entree",
#         "id": "1",
#     },
#     {
#         "name": "Chocolate Cake",
#         "description": "made with Dutch Chocolate",
#         "price": "$3.99",
#         "course": "Dessert",
#         "id": "2",
#     },
#     {
#         "name": "Caesar Salad",
#         "description": "with fresh organic vegetables",
#         "price": "$5.99",
#         "course": "Entree",
#         "id": "3",
#     },
#     {
#         "name": "Iced Tea",
#         "description": "with lemon",
#         "price": "$.99",
#         "course": "Beverage",
#         "id": "4",
#     },
#     {
#         "name": "Spinach Dip",
#         "description": "creamy dip with fresh spinach",
#         "price": "$1.99",
#         "course": "Appetizer",
#         "id": "5",
#     },
# ]
# item = {
#     "name": "Cheese Pizza",
#     "description": "made with fresh cheese",
#     "price": "$5.99",
#     "course": "Entree",
# }
# items = []


app = Flask(__name__)

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def welcome():
    return "welcome to the new restaurant app"


@app.route("/restaurant/")
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/restaurant/new/", methods=["GET", "POST"])
def newRestaurant():
    if request.method == "POST":
        newRestaurant = Restaurant(
            name=request.form["name"],
        )
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for("showRestaurants"))

    else:
        return render_template(
            "newRestaurant.html",
        )


@app.route("/restaurant/<int:restaurant_id>/edit/", methods=["GET", "POST"])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        if request.form["name"]:
            editedRestaurant.name = request.form["name"]
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant has been edited")
        return redirect(url_for("showRestaurants"))

    else:
        return render_template("editRestaurant.html", restaurant_id=restaurant_id)


@app.route("/restaurant/<int:restaurant_id>/delete/", methods=["GET", "POST"])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant has been deleted")
        return redirect(url_for("showRestaurants", restaurant_id=restaurant_id))
    else:
        return render_template("deleteRestaurant.html", restaurant_id=restaurant_id)


@app.route("/restaurant/<int:restaurant_id>/menu/")
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template("menu.html", items=items, restaurant=restaurant)


@app.route("/restaurant/<int:restaurant_id>/menu/new/", methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newMenu = MenuItem(
            name=request.form["name"],
            description=request.form["description"],
            course=request.form["course"],
            price=request.form["price"],
            restaurant_id=restaurant_id,
        )
        session.add(newMenu)
        session.commit()
        flash("New menu has been added")

        return redirect(url_for("showMenu", restaurant_id=restaurant_id))
    else:
        return render_template("newmenuitem.html", restaurant_id=restaurant_id)


@app.route(
    "/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/", methods=["GET", "POST"]
)
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        if request.form["name"]:
            editedItem.name = request.form["name"]
        if request.form["description"]:
            editedItem.name = request.form["description"]
        if request.form["price"]:
            editedItem.name = request.form["price"]
        if request.form["course"]:
            editedItem.name = request.form["course"]
        session.add(editedItem)
        session.commit()
        flash("Menu has been edited")

        return redirect(url_for("showMenu", restaurant_id=restaurant_id))
    else:
        return render_template(
            "editmenuitem.html",
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            item=editedItem,
        )


@app.route(
    "/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/",
    methods=["GET", "POST"],
)
def deleteMenuItem(restaurant_id, menu_id):
    menuToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        session.delete(menuToDelete)
        session.commit()
        flash("Menu has been deleted")

        return redirect(url_for("showMenu", restaurant_id=restaurant_id))
    return render_template(
        "deletemenuitem.html",
        restaurant_id=restaurant_id,
        menu_id=menu_id,
        item=menuToDelete,
    )


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
