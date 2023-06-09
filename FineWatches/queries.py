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


from FineWatches import db_cursor, conn
from FineWatches import User, BrandRep, Customer, Watches, Sell, WatchOrder

# INSERT QUERIES
def insert_user(user: User):
    sql = """
    INSERT INTO Users(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
    conn.commit()


def insert_brandrep(brandrep: BrandRep):
    sql = """
    INSERT INTO BrandRep(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (brandrep.user_name, brandrep.full_name, brandrep.password))
    conn.commit()

def insert_customer(customer: Customer):
    sql = """
    INSERT INTO Customers(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (customer.user_name, customer.full_name, customer.password))
    conn.commit()

def insert_watch(watch: Watches):
    sql = """
    INSERT INTO Watches(brand, model, "Case Material", "Strap Material", "Movement Type",
    "Water Resistance", "Case Diameter", "Case Thickness", "Band Width", "Dial Color",
    "Crystal Material", "Complications", "Power Reserve", price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING pk
    """
    db_cursor.execute(sql, (
        watch.brand,
        watch.model,
        watch["Case Material"],
        watch["Strap Material"],
        watch["Movement Type"],
        watch["Water Resistance"],
        watch["Case Diameter"],
        watch["Case Thickness"],
        watch["Band Width"],
        watch["Dial Color"],
        watch["Crystal Material"],
        watch.Complications,
        watch["Power Reserve"],
        watch.price      
    ))
    
    conn.commit()
    return db_cursor.fetchone().get('pk') if db_cursor.rowcount > 0 else None


def insert_sell(sell: Sell):
    sql = """
    INSERT INTO Sell(brandrep_pk, watches_pk)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (sell.brandrep_pk, sell.watches_pk,))
    conn.commit()

def insert_produce_order(order: WatchOrder):
    sql = """
    INSERT INTO ProduceOrder(watches_pk, brandrep_pk, customer_pk)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (
        order.watches_pk,
        order.brandrep_pk,
        order.customer_pk,
    ))
    


# SELECT QUERIES
def get_user_by_pk(pk):
    sql = """
    SELECT * FROM Users
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_brandrep_by_pk(pk):
    sql = """
    SELECT * FROM BrandRep
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    brandrep = BrandRep(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return brandrep

def get_watches_by_filters(brand=None, model=None,
                           brandrep_pk=None, brandrep_name=None, price=None):
    sql = """
    SELECT * FROM vw_watches
    WHERE
    """
    conditionals = []
    if brand:
        conditionals.append(f"category='{brand}'")
    if model:
        conditionals.append(f"model='{model}'")
    if brandrep_pk:
        conditionals.append(f"brandrep_pk = '{brandrep_pk}'")
    if brandrep_name:
        conditionals.append(f"farmer_name LIKE '%{brandrep_name}%'")
    if price:
        conditionals.append(f"price <= {price}")

    args_str = ' AND '.join(conditionals)
    order = " ORDER BY price "
    db_cursor.execute(sql + args_str + order)
    watches = [Watches(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return watches


def get_customer_by_pk(pk):
    sql = """
    SELECT * FROM Customers
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    customer = Customer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return customer

def get_watches_by_pk(pk):
    sql = """
    SELECT watches_pk as pk, * FROM vw_watches
    WHERE watches_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    watches = Watches(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return watches


def get_all_watches_by_brandrep(pk):
    sql = """
    SELECT * FROM vw_watches
    WHERE brandrep_pk = %s
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql, (pk,))
    watches = [Watches(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return watches


def get_user_by_user_name(user_name):
    sql = """
    SELECT * FROM Users
    WHERE user_name = %s
    """
    db_cursor.execute(sql, (user_name,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_all_watches():
    sql = """
    SELECT watches_pk as pk, brand, model, "Case Material", "Strap Material", "Movement Type",
    "Water Resistance","Case Diameter","Case Thickness","Band Width","Dial Color","Crystal Material",
    Complications,"Power Reserve",price, brandrep_name, available, brandrep_pk
    FROM vw_waches
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql)
    watches = [Watches(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return watches


def get_available_watches():
    sql = """
    SELECT * FROM vw_watches
    WHERE available = true
    ORDER BY price  
    """
    db_cursor.execute(sql)
    watches = [Watches(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return watches

def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM WatchOrder wo
    JOIN Watches w ON w.pk = wo.produce_pk
    WHERE customer_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    orders = [WatchOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return orders


# UPDATE QUERIES
def update_sell(available, watches_pk, brandrep_pk):
    sql = """
    UPDATE Sell
    SET available = %s
    WHERE watches_pk = %s
    AND brandrep_pk = %s
    """
    db_cursor.execute(sql, (available, watches_pk, brandrep_pk))
    conn.commit()


