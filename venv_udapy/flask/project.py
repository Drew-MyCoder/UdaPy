# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

# Create session and connect to DB
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def welcome():
    return "welcome to the restaurant app"


# @app.route("/hello")
# def HelloWorld():
#     restaurant = session.query(Restaurant).first()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
#     output = ""
#     for i in items:
#         output += i.name
#         output += "</br>"

#     return output


# @app.route("/hello/price")
# def ItemMenu():
#     restaurant = session.query(Restaurant).first()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
#     output = ""
#     for i in items:
#         output += i.name
#         output += "</br>"
#         output += i.price
#         output += "</br>"
#         output += i.description
#         output += "</br>"
#         output += "</br>"
#     return output


@app.route("/restaurants/<int:restaurant_id>/JSON/")
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/")
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route("/restaurants/<int:restaurant_id>/")
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template(
        "menu.html", restaurant=restaurant, items=items, restaurant_id=restaurant_id
    )
    # output = ""
    # for i in items:
    #     output += i.name
    #     output += "</br>"
    #     output += i.price
    #     output += "</br>"
    #     output += i.description
    #     output += "</br>"
    #     output += "</br>"
    # return output


# Task 1: Create route for newMenuItem function here


@app.route("/restaurants/<int:restaurant_id>/new/", methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(
            name=request.form["name"],
            description=request.form["description"],
            price=request.form["price"],
            course=request.form["course"],
            restaurant_id=restaurant_id,
        )
        session.add(newItem)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        return render_template("newmenuitem.html", restaurant_id=restaurant_id)


# Task 2: Create route for edit menuItem function here


@app.route(
    "/restaurants/<int:restaurant_id>/<int:menu_id>/edit/", methods=["GET", "POST"]
)
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        if request.form["name"]:
            editedItem.name = request.form["name"]
        # if request.form["description"]:
        #     editedItem.description = request.form["description"]
        # if request.form["price"]:
        #     editedItem.price = request.form["price"]
        # if request.form["course"]:
        #     editedItem.course = request.form["course"]
        session.add(editedItem)
        session.commit()
        flash("Menu item has been edited")
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        return render_template(
            "editmenuitem.html",
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            item=editedItem,
        )


# Task 3: Create route for delete menuItem function here


@app.route(
    "/restaurants/<int:restaurant_id>/<int:menu_id>/delete/", methods=["GET", "POST"]
)
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        session.delete(itemToDelete)
        session.commit()
        flash("Menu item has been deleted")
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        return render_template("deletemenuitem.html", item=itemToDelete)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
