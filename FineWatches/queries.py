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

def insert_watch_order(order: WatchOrder):
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


