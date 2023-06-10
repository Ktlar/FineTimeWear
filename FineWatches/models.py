# import sqlite3

# # Watch model class
# class Watch:
#     def __init__(self, brand, model, caseMaterial, strapMaterial, movementType, caseDiameter, caseThickness, waterResistance, price):
#         self.brand = brand
#         self.model = model
#         self.specification = caseMaterial
#         self.strapMaterial = strapMaterial
#         self.MovementType = movementType
#         self.caseDiameter = caseDiameter
#         self.caseThickness = caseThickness

#         self.waterResistance = waterResistance
#         self.price = price

# # Function to establish a connection with the database
# def create_connection():
#     conn = None
#     try:
#         conn = sqlite3.connect('luxury_watches.db')
#         print("Connection to the database successful")
#     except sqlite3.Error as e:
#         print(e)

#     return conn

# # Function to retrieve all watches from the database
# def get_all_watches():
#     conn = create_connection()
#     try:
#         cursor = conn.execute("SELECT * FROM watches")
#         watches = []
#         for row in cursor.fetchall():
#             watch = Watch(row[1], row[2], row[3], row[4], row[6], row[14])
#             watches.append(watch)
#         return watches
#     except sqlite3.Error as e:
#         print(e)
#     finally:
#         conn.close()

# # Function to retrieve a specific watch by its ID
# def get_watch_by_id(watch_id):
#     conn = create_connection()
#     try:
#         cursor = conn.execute("SELECT * FROM watches WHERE id = ?", (watch_id,))
#         row = cursor.fetchone()
#         if row:
#             watch = Watch(row[1], row[2], row[3], row[4], row[6], row[14])
#             return watch
#         else:
#             return None
#     except sqlite3.Error as e:
#         print(e)
#     finally:
#         conn.close()

"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from FineWatches import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Watches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    case_material = db.Column(db.String(50), nullable=False)
    strap_material = db.Column(db.String(50), nullable=False)
    water_resistance = db.Column(db.String(50), nullable=False)
    movement_type = db.Column(db.String(50), nullable=False)
    case_diameter = db.Column(db.String(50), nullable=False)
    case_thickness = db.Column(db.String(50), nullable=False)
    band_width = db.Column(db.String(50), nullable=False)
    dial_color = db.Column(db.String(50), nullable=False)
    crystal_material = db.Column(db.String(50), nullable=False)
    complications = db.Column(db.String(50), nullable=False)
    power_reserve = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    brandrep_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    watches = db.relationship('Watch', secondary='customer_watch', backref='customers')


class CustomerWatch(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    watch_id = db.Column(db.Integer, db.ForeignKey('watch.id'), primary_key=True)


class BrandRep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    watches = db.relationship('Watch', backref='brand_rep')
"""

from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

from FineWatches import login_manager, db_cursor, conn, app


@login_manager.user_loader
def load_user(user_id):
    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE pk = %s
    """).format(sql.Identifier('pk'))

    db_cursor.execute(user_sql, (int(user_id),))
    return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


class ModelUserMixin(dict, UserMixin):
    @property
    def id(self):
        return self.pk


class ModelMixin(dict):
    pass


class User(ModelUserMixin):
    def __init__(self, user_data: Dict):
        super(User, self).__init__(user_data)
        self.pk = user_data.get('pk')
        self.full_name = user_data.get('full_name')
        self.user_name = user_data.get('user_name')
        self.password = user_data.get('password')


class Customer(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


class BrandRep(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


if __name__ == '__main__':
    user_data = dict(full_name='a', user_name='b', password='c')
    user = BrandRep(user_data)
    print(user)


class Watches(ModelMixin):
    def __init__(self, watch_data: Dict):
        super(Watches, self).__init__(watch_data)
        self.pk = watch_data.get('pk')
        self.brand = watch_data.get('brand')
        self.model = watch_data.get('model')
        self.caseMaterial = watch_data.get('Case Material')
        self.strapMaterial = watch_data.get('Strap Material')
        self.movementType = watch_data.get('Movement Type')
        self.waterResistance = watch_data.get('Water Resistance')
        self.caseDiameter = watch_data.get('Case Diameter')
        self.caseThickness = watch_data.get('Case Thickness')
        self.bandWidth = watch_data.get('Band Width')
        self.dialColor = watch_data.get('Dial Color')
        self.crystalMaterial = watch_data.get('Crystal Material')
        self.complications = watch_data.get('Complications')
        self.powerReserve = watch_data.get('Power Reserve')
        self.price = watch_data.get('price')
        # From JOIN w/ Sell relation
        self.available = watch_data.get('available')
        self.brandrep_name = watch_data.get('brandrep_name')
        self.brandrep_pk = watch_data.get('brandrep_pk')




class Sell(ModelMixin):
    def __init__(self, sell_data: Dict):
        super(Sell, self).__init__(sell_data)
        self.available = sell_data.get('available')
        self.brandrep_pk = sell_data.get('brandrep_pk')
        self.watches_pk = sell_data.get('watches_pk')


class WatchOrder(ModelMixin):
    def __init__(self, watch_order_data: Dict):
        super(WatchOrder, self).__init__(watch_order_data)
        self.pk = watch_order_data.get('pk')
        self.customer_pk = watch_order_data.get('customer_pk')
        self.brandrep_pk = watch_order_data.get('brandrep_pk')
        self.watches_pk = watch_order_data.get('watches_pk')