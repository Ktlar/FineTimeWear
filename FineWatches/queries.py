from FineWatches import db_cursor, conn
from FineWatches.models import User, BrandRep, Customer, Watches, Sell, WatchOrder


# INSERT QUERIES
def insert_object(obj, table_name):
    sql = f"""
    INSERT INTO {table_name} {obj.get_insert_columns()}
    VALUES {obj.get_insert_values()}
    """
    db_cursor.execute(sql, obj.get_insert_parameters())
    conn.commit()


def insert_user(user):
    insert_object(user, 'Users')


def insert_brandrep(brandrep):
    insert_object(brandrep, 'BrandRep')


def insert_customer(customer):
    insert_object(customer, 'Customers')


def insert_watch(watch):
    insert_object(watch, 'Watches')


def insert_sell(sell):
    insert_object(sell, 'Sell')


def insert_watch_order(order):
    insert_object(order, 'ProduceOrder')


# SELECT QUERIES
def get_object_by_pk(table_name, pk):
    sql = f"""
    SELECT * FROM {table_name}
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    result = db_cursor.fetchone()
    obj = None
    if result:
        if table_name == 'Users':
            obj = User(result)
        elif table_name == 'BrandRep':
            obj = BrandRep(result)
        elif table_name == 'Customers':
            obj = Customer(result)
        elif table_name == 'Watches':
            obj = Watches(result)
        elif table_name == 'Sell':
            obj = Sell(result)
        elif table_name == 'ProduceOrder':
            obj = WatchOrder(result)
    return obj


def get_user_by_pk(pk):
    return get_object_by_pk('Users', pk)


def get_brandrep_by_pk(pk):
    return get_object_by_pk('BrandRep', pk)


def get_customer_by_pk(pk):
    return get_object_by_pk('Customers', pk)


def get_watches_by_pk(pk):
    return get_object_by_pk('Watches', pk)


def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM WatchOrder wo
    JOIN Watches w ON w.pk = wo.produce_pk
    WHERE customer_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    orders = [WatchOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return orders


def get_watches_by_filters(brand=None, model=None, brandrep_pk=None, brandrep_name=None, price=None):
    sql = """
    SELECT * FROM vw_watches
    WHERE 1 = 1
    """
    conditionals = []
    args = []
    
    if brand:
        conditionals.append("brand = %s")
        args.append(brand)
    if model:
        conditionals.append("model = %s")
        args.append(model)
    if brandrep_pk:
        conditionals.append("brandrep_pk = %s")
        args.append(brandrep_pk)
    if brandrep_name:
        conditionals.append("brandrep_name LIKE %s")
        args.append(f"%{brandrep_name}%")
    if price:
        conditionals.append("price::integer <= %s")
        args.append(price)

    args_str = " AND ".join(conditionals)
    order = " ORDER BY price"

    query = sql + (" AND " + args_str if args_str else "") + order
    db_cursor.execute(query, tuple(args))
    
    watches = [Watches(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
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
    FROM vw_watches
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