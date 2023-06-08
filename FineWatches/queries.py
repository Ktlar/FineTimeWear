"""The file queries.py appears to contain various functions that execute SQL queries on a PostgreSQL database using the db_cursor 
and conn objects from the GreenGroceries module. Let's go through the different sections and understand what each function does:

INSERT QUERIES:
The insert_user, insert_farmer, and insert_customer functions insert records into their respective tables (Users, Farmers, Customers).
The insert_produce function inserts a record into the Produce table and returns the primary key (pk) of the inserted row.
The insert_sell function inserts a record into the Sell table, which seems to associate a farmer 
(farmer_pk) with a produce item (produce_pk).
The insert_produce_order function inserts a record into the ProduceOrder table, associating a 
produce item (produce_pk), farmer (farmer_pk), and customer (customer_pk).
SELECT QUERIES:
The get_user_by_pk, get_farmer_by_pk, and get_customer_by_pk functions retrieve records 
from their respective tables based on the provided primary key (pk).
The get_produce_by_filters function retrieves produce records from the vw_produce view based 
on various filter conditions (e.g., category, item, variety, farmer, price).
The get_produce_by_pk function retrieves a single produce record based on the provided primary key (pk).
The get_all_produce_by_farmer function retrieves all produce records associated with a specific farmer (pk).
The get_user_by_user_name function retrieves a user record based on the provided username (user_name).
The get_all_produce function retrieves all produce records from the vw_produce view.
The get_available_produce function retrieves all available produce records from the vw_produce view.
The get_orders_by_customer_pk function retrieves produce orders associated with a specific customer (pk).
UPDATE QUERIES:
The update_sell function updates the available column of the Sell table for a 
specific produce item (produce_pk) and farmer (farmer_pk).
These functions provide an interface to interact with the database by executing SQL queries 
and returning the results or modifying the data. They can be used in conjunction with other 
parts of the application to handle database operations.
Note: The code snippets provided give an overview of the functionality, but the specific 
implementation of the User, Farmer, Customer, Produce, Sell, and ProduceOrder classes and 
the initialization of the db_cursor and conn objects are not shown in this file. """

#from GreenGroceries import db_cursor, conn
#from GreenGroceries.models import User, Farmer, Customer, Produce, Sell, ProduceOrder


# INSERT QUERIES
#def insert_user(user: User):
#     sql = """
#     INSERT INTO Users(user_name, full_name, password)
#     VALUES (%s, %s, %s)
#     """
#     db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
#     conn.commit()


# def insert_farmer(farmer: Farmer):
#     sql = """
#     INSERT INTO Farmers(user_name, full_name, password)
#     VALUES (%s, %s, %s)
#     """
#     db_cursor.execute(sql, (farmer.user_name, farmer.full_name, farmer.password))
#     conn.commit()


# def insert_customer(customer: Customer):
#     sql = """
#     INSERT INTO Customers(user_name, full_name, password)
#     VALUES (%s, %s, %s)
#     """
#     db_cursor.execute(sql, (customer.user_name, customer.full_name, customer.password))
#     conn.commit()


# def insert_produce(produce: Produce):
#     sql = """
#     INSERT INTO Produce(category, item, unit, variety, price)
#     VALUES (%s, %s, %s, %s, %s) RETURNING pk
#     """
#     db_cursor.execute(sql, (
#         produce.category,
#         produce.item,
#         produce.unit,
#         produce.variety,
#         produce.price
#     ))
#     conn.commit()
#     return db_cursor.fetchone().get('pk') if db_cursor.rowcount > 0 else None


# def insert_sell(sell: Sell):
#     sql = """
#     INSERT INTO Sell(farmer_pk, produce_pk)
#     VALUES (%s, %s)
#     """
#     db_cursor.execute(sql, (sell.farmer_pk, sell.produce_pk,))
#     conn.commit()


# def insert_produce_order(order: ProduceOrder):
#     sql = """
#     INSERT INTO ProduceOrder(produce_pk, farmer_pk, customer_pk)
#     VALUES (%s, %s, %s)
#     """
#     db_cursor.execute(sql, (
#         order.produce_pk,
#         order.farmer_pk,
#         order.customer_pk,
#     ))
#     conn.commit()


# # SELECT QUERIES
# def get_user_by_pk(pk):
#     sql = """
#     SELECT * FROM Users
#     WHERE pk = %s
#     """
#     db_cursor.execute(sql, (pk,))
#     user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
#     return user


# def get_farmer_by_pk(pk):
#     sql = """
#     SELECT * FROM Farmers
#     WHERE pk = %s
#     """
#     db_cursor.execute(sql, (pk,))
#     farmer = Farmer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
#     return farmer


# def get_produce_by_filters(category=None, item=None, variety=None,
#                            farmer_pk=None, farmer_name=None, price=None):
#     sql = """
#     SELECT * FROM vw_produce
#     WHERE
#     """
#     conditionals = []
#     if category:
#         conditionals.append(f"category='{category}'")
#     if item:
#         conditionals.append(f"item='{item}'")
#     if variety:
#         conditionals.append(f"variety = '{variety}'")
#     if farmer_pk:
#         conditionals.append(f"farmer_pk = '{farmer_pk}'")
#     if farmer_name:
#         conditionals.append(f"farmer_name LIKE '%{farmer_name}%'")
#     if price:
#         conditionals.append(f"price <= {price}")

#     args_str = ' AND '.join(conditionals)
#     order = " ORDER BY price "
#     db_cursor.execute(sql + args_str + order)
#     produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
#     return produce


# def get_customer_by_pk(pk):
#     sql = """
#     SELECT * FROM Customers
#     WHERE pk = %s
#     """
#     db_cursor.execute(sql, (pk,))
#     customer = Customer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
#     return customer


# def get_produce_by_pk(pk):
#     sql = """
#     SELECT produce_pk as pk, * FROM vw_produce
#     WHERE produce_pk = %s
#     """
#     db_cursor.execute(sql, (pk,))
#     produce = Produce(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
#     return produce


# def get_all_produce_by_farmer(pk):
#     sql = """
#     SELECT * FROM vw_produce
#     WHERE farmer_pk = %s
#     ORDER BY available DESC, price
#     """
#     db_cursor.execute(sql, (pk,))
#     produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
#     return produce


# def get_user_by_user_name(user_name):
#     sql = """
#     SELECT * FROM Users
#     WHERE user_name = %s
#     """
#     db_cursor.execute(sql, (user_name,))
#     user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
#     return user


# def get_all_produce():
#     sql = """
#     SELECT produce_pk as pk, category, item, variety, unit, price, farmer_name, available, farmer_pk
#     FROM vw_produce
#     ORDER BY available DESC, price
#     """
#     db_cursor.execute(sql)
#     produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
#     return produce


# def get_available_produce():
#     sql = """
#     SELECT * FROM vw_produce
#     WHERE available = true
#     ORDER BY price  
#     """
#     db_cursor.execute(sql)
#     produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
#     return produce


# def get_orders_by_customer_pk(pk):
#     sql = """
#     SELECT * FROM ProduceOrder po
#     JOIN Produce p ON p.pk = po.produce_pk
#     WHERE customer_pk = %s
#     """
#     db_cursor.execute(sql, (pk,))
#     orders = [ProduceOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
#     return orders


# # UPDATE QUERIES
# def update_sell(available, produce_pk, farmer_pk):
#     sql = """
#     UPDATE Sell
#     SET available = %s
#     WHERE produce_pk = %s
#     AND farmer_pk = %s
#     """
#     db_cursor.execute(sql, (available, produce_pk, farmer_pk))
#     conn.commit()


import sqlite3

# Function to establish a connection with the database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('luxury_watches.db')
        print("Connection to the database successful")
    except sqlite3.Error as e:
        print(e)

    return conn

# Function to create the watch table in the database
def create_watch_table():
    conn = create_connection()
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS watches
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     brand TEXT NOT NULL,
                     model TEXT NOT NULL,
                     specification TEXT,
                     price INTEGER);''')
        print("Watch table created successfully")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

# Function to insert a new watch into the database
def insert_watch(brand, model, specification, price):
    conn = create_connection()
    try:
        conn.execute("INSERT INTO watches (brand, model, specification, price) VALUES (?, ?, ?, ?)",
                     (brand, model, specification, price))
        conn.commit()
        print("Watch inserted successfully")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

# Function to retrieve all watches from the database
def get_all_watches():
    conn = create_connection()
    try:
        cursor = conn.execute("SELECT * FROM watches")
        watches = cursor.fetchall()
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
        watch = cursor.fetchone()
        return watch
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


