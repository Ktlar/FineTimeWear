import sqlite3

# Watch model class
class Watch:
    def __init__(self, brand, model, caseMaterial, strapMaterial, movementType, caseDiameter, caseThickness, waterResistance, price):
        self.brand = brand
        self.model = model
        self.specification = caseMaterial
        self.strapMaterial = strapMaterial
        self.MovementType = movementType
        self.caseDiameter = caseDiameter
        self.caseThickness = caseThickness

        self.waterResistance = waterResistance
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
            watch = Watch(row[1], row[2], row[3], row[4], row[6], row[14])
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
            watch = Watch(row[1], row[2], row[3], row[4], row[6], row[14])
            return watch
        else:
            return None
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
