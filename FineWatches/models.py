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


class Watch(db.Model):
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
