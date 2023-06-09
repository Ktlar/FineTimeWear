"""The models.py file contains the model classes used in the GreenGroceries web application.
Let's go through each model and its properties:

ModelUserMixin:

Purpose: A mixin class that provides common functionality for user models.
Properties:
id: Returns the primary key (pk) of the user.
ModelMixin:

Purpose: A mixin class that provides a base for other model classes.
User:

Purpose: Represents a user in the application.
Properties:
pk: Primary key of the user.
full_name: Full name of the user.
user_name: Username of the user.
password: Password of the user.
Customer:

Purpose: Represents a customer in the application. Inherits from the User class.
Farmer:

Purpose: Represents a farmer in the application. Inherits from the User class.
Produce:

Purpose: Represents a produce item in the application.
Properties:
pk: Primary key of the produce item.
category: Category of the produce item.
item: Subcategory of the produce item.
unit: Unit of measurement for the produce item.
variety: Variety of the produce item.
price: Price of the produce item.
available: Availability status of the produce item.
farmer_name: Name of the farmer selling the produce item.
farmer_pk: Primary key of the farmer selling the produce item.
Sell:

Purpose: Represents a selling relationship between a farmer and a produce item.
Properties:
available: Availability status of the produce item being sold.
farmer_pk: Primary key of the farmer selling the produce item.
produce_pk: Primary key of the produce item being sold.
ProduceOrder:

Purpose: Represents an order for a produce item.
Properties:
pk: Primary key of the produce order.
customer_pk: Primary key of the customer placing the order.
farmer_pk: Primary key of the farmer fulfilling the order.
produce_pk: Primary key of the produce item being ordered.
The models.py file also includes a load_user function that is used by Flask-Login to load a user object based on the user ID.

At the end of the file, there is a test code snippet that creates a Farmer instance and prints it.

These model classes represent the data entities in the application and provide a convenient way to work with the data retrieved
 from the database in a structured manner.
 """
 
from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

# from GreenGroceries import login_manager, db_cursor, conn, app


# @login_manager.user_loader
# def load_user(user_id):
#     user_sql = sql.SQL("""
#     SELECT * FROM Users
#     WHERE pk = %s
#     """).format(sql.Identifier('pk'))

#     db_cursor.execute(user_sql, (int(user_id),))
#     return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


# class ModelUserMixin(dict, UserMixin):
#     @property
#     def id(self):
#         return self.pk


# class ModelMixin(dict):
#     pass


# class User(ModelUserMixin):
#     def __init__(self, user_data: Dict):
#         super(User, self).__init__(user_data)
#         self.pk = user_data.get('pk')
#         self.full_name = user_data.get('full_name')
#         self.user_name = user_data.get('user_name')
#         self.password = user_data.get('password')


# class Customer(User):
#     def __init__(self, user_data: Dict):
#         super().__init__(user_data)


# class Farmer(User):
#     def __init__(self, user_data: Dict):
#         super().__init__(user_data)


# if __name__ == '__main__':
#     user_data = dict(full_name='a', user_name='b', password='c')
#     user = Farmer(user_data)
#     print(user)


# class Produce(ModelMixin):
#     def __init__(self, produce_data: Dict):
#         super(Produce, self).__init__(produce_data)
#         self.pk = produce_data.get('pk')
#         self.category = produce_data.get('category')
#         self.item = produce_data.get('item')
#         self.unit = produce_data.get('unit')
#         self.variety = produce_data.get('variety')
#         self.price = produce_data.get('price')
#         # From JOIN w/ Sell relation
#         self.available = produce_data.get('available')
#         self.farmer_name = produce_data.get('farmer_name')
#         self.farmer_pk = produce_data.get('farmer_pk')


# class Sell(ModelMixin):
#     def __init__(self, sell_data: Dict):
#         super(Sell, self).__init__(sell_data)
#         self.available = sell_data.get('available')
#         self.farmer_pk = sell_data.get('farmer_pk')
#         self.produce_pk = sell_data.get('produce_pk')


# class ProduceOrder(ModelMixin):
#     def __init__(self, produce_order_data: Dict):
#         super(ProduceOrder, self).__init__(produce_order_data)
#         self.pk = produce_order_data.get('pk')
#         self.customer_pk = produce_order_data.get('customer_pk')
#         self.farmer_pk = produce_order_data.get('farmer_pk')
#         self.produce_pk = produce_order_data.get('produce_pk')

import sqlite3

# Watch model class
class Watch:
    def __init__(self, id, brand, model, specification, price):
        self.id = id
        self.brand = brand
        self.model = model
        self.specification = specification
        self.price = price

# Function to establish a connection with the database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('luxury_watches.db')
        print("Connection to the database successful")
    except sqlite3.Error as e:
        print(e)

    return conn

# Function to retrieve all watches from the database
def get_all_watches():
    conn = create_connection()
    try:
        cursor = conn.execute("SELECT * FROM watches")
        watches = []
        for row in cursor.fetchall():
            watch = Watch(row[0], row[1], row[2], row[3], row[4])
            watches.append(watch)
        return watches
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

# Function to retrieve a specific watch by its ID
def get_watch_by_id(watch_id):
    conn = create_connection()
    try:
        cursor = conn.execute("SELECT * FROM watches WHERE id = ?", (watch_id,))
        row = cursor.fetchone()
        if row:
            watch = Watch(row[0], row[1], row[2], row[3], row[4])
            return watch
        else:
            return None
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
