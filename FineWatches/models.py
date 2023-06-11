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
        super().__init__(user_data)
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


class Watches(ModelMixin):
    def __init__(self, watch_data: Dict):
        super().__init__(watch_data)
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
        super().__init__(sell_data)
        self.available = sell_data.get('available')
        self.brandrep_pk = sell_data.get('brandrep_pk')
        self.watches_pk = sell_data.get('watches_pk')


class WatchOrder(ModelMixin):
    def __init__(self, watch_order_data: Dict):
        super().__init__(watch_order_data)
        self.pk = watch_order_data.get('pk')
        self.customer_pk = watch_order_data.get('customer_pk')
        self.brandrep_pk = watch_order_data.get('brandrep_pk')
        self.watches_pk = watch_order_data.get('watches_pk')


if __name__ == '__main__':
    user_data = dict(full_name='a', user_name='b', password='c')
    user = BrandRep(user_data)
    print(user)


class WatchOrder(ModelMixin):
    def __init__(self, watch_order_data: Dict):
        super(WatchOrder, self).__init__(watch_order_data)
        self.pk = watch_order_data.get('pk')
        self.customer_pk = watch_order_data.get('customer_pk')
        self.brandrep_pk = watch_order_data.get('brandrep_pk')
        self.watches_pk = watch_order_data.get('watches_pk')