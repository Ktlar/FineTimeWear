import psycopg2

hostname = 'localhost'
database = 'FineWatches'
username = 'postgres'
pwd = 'eplavelta'
port_id = 5432
conn = None
cur = None
try:
    conn = psycopg2.connect(
        host = 'localhost',
        dbname = 'FineWatches',
        user = 'postgres',
        password = 'eplavelta',
        port = port_id
        )

    cur = conn.cursor()

    create_watches =''' CREATE TABLE IF NOT EXISTS watches2 (
                        id  int PRIMARY KEY,
                        brand VARCHAR(40) NOT NULL,
                        model VARCHAR(40) NOT NULL,
                        "Case Material" VARCHAR(40) NOT NULL,
                        "Strap Material" VARCHAR(40) NOT NULL,
                        "Movement Type" VARCHAR(40) NOT NULL,
                        "Water Resistance" VARCHAR(40) NOT NULL,
                        "Case Diameter" VARCHAR(40) NOT NULL,
                        "Case Thickness" VARCHAR(40) NOT NULL,
                        "Band Width" VARCHAR(40) NOT NULL,
                        "Dial Color" VARCHAR(40) NOT NULL,
                        "Crystal Material" VARCHAR(40) NOT NULL,
                        "Complication" VARCHAR(40) NOT NULL,
                        "Power Reserve" VARCHAR(40) NOT NULL,
                        price VARCHAR(40) NOT NULL) '''

    cur.execute(create_watches)

    insert_watches = 'INSERT INTO watches'

    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()