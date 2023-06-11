from FineWatches import db_cursor, conn
from FineWatches.models import User, BrandRep, Customer, Watches, Sell, WatchOrder


# INSERT QUERIES
def insert_record(table_name, **kwargs):
    columns = ', '.join(kwargs.keys())
    placeholders = ', '.join(['%s'] * len(kwargs))
    values = tuple(kwargs.values())

    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    db_cursor.execute(sql, values)
    conn.commit()


def insert_user(user: User):
    insert_record("Users", user_name=user.user_name, full_name=user.full_name, password=user.password)


def insert_brandrep(brandrep: BrandRep):
    insert_record("BrandRep", user_name=brandrep.user_name, full_name=brandrep.full_name, password=brandrep.password)


def insert_customer(customer: Customer):
    insert_record("Customers", user_name=customer.user_name, full_name=customer.full_name, password=customer.password)


def insert_watch(watch: Watches):
    insert_record("Watches", brand=watch.brand, model=watch.model, **watch.attributes, price=watch.price)


def insert_sell(sell: Sell):
    insert_record("Sell", brandrep_pk=sell.brandrep_pk, watches_pk=sell.watches_pk)


def insert_watch_order(order: WatchOrder):
    insert_record("ProduceOrder", watches_pk=order.watches_pk, brandrep_pk=order.brandrep_pk, customer_pk=order.customer_pk)


# SELECT QUERIES
def execute_select_query(sql, *params):
    db_cursor.execute(sql, params)
    results = db_cursor.fetchall()
    return results


def get_user_by_pk(pk):
    sql = "SELECT * FROM Users WHERE pk = %s"
    results = execute_select_query(sql, pk)
    return User(results[0]) if results else None


def get_brandrep_by_pk(pk):
    sql = "SELECT * FROM BrandRep WHERE pk = %s"
    results = execute_select_query(sql, pk)
    return BrandRep(results[0]) if results else None


def get_watches_by_filters(brand=None, model=None, brandrep_pk=None, brandrep_name=None, price=None):
    conditionals = []
    if brand:
        conditionals.append("brand = %s")
    if model:
        conditionals.append("model = %s")
    if brandrep_pk:
        conditionals.append("brandrep_pk = %s")
    if brandrep_name:
        conditionals.append("brandrep_name LIKE %s")
    if price:
        conditionals.append("price <= %s")

    args = [arg for arg in (brand, model, brandrep_pk, f"%{brandrep_name}%", price) if arg is not None]
    conditions = " AND ".join(conditionals)
    order_by = "ORDER BY price"

    sql = f"SELECT * FROM vw_watches WHERE {conditions} {order_by}"
    results = execute_select_query(sql, *args)
    return [Watches(res) for res in results]


def get_customer_by_pk(pk):
    sql = "SELECT * FROM Customers WHERE pk = %s"
    results = execute_select_query(sql, pk)
    return Customer(results[0]) if results else None


def get_watches_by_pk(pk):
    sql = "SELECT watches_pk as pk, * FROM vw_watches WHERE watches_pk = %s"
    results = execute_select_query(sql, pk)
    return Watches(results[0]) if results else None


def get_all_watches_by_brandrep(pk):
    sql = "SELECT * FROM vw_watches WHERE brandrep_pk = %s ORDER BY available DESC, price"
    results = execute_select_query(sql, pk)
    return [Watches(res) for res in results]


def get_user_by_user_name(user_name):
    sql = "SELECT * FROM Users WHERE user_name = %s"
    results = execute_select_query(sql, user_name)
    return User(results[0]) if results else None


def get_all_watches():
    sql = """
    SELECT watches_pk as pk, brand, model, "Case Material", "Strap Material", "Movement Type",
    "Water Resistance","Case Diameter","Case Thickness","Band Width","Dial Color","Crystal Material",
    Complications,"Power Reserve",price, brandrep_name, available, brandrep_pk
    FROM vw_watches
    ORDER BY available DESC, price
    """
    results = execute_select_query(sql)
    return [Watches(res) for res in results]


def get_available_watches():
    sql = "SELECT * FROM vw_watches WHERE available = true ORDER BY price"
    results = execute_select_query(sql)
    return [Watches(res) for res in results]


def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM WatchOrder wo
    JOIN Watches w ON w.pk = wo.produce_pk
    WHERE customer_pk = %s
    """
    results = execute_select_query(sql, pk)
    return [WatchOrder(res) for res in results]


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