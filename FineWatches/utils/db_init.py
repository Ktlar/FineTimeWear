import psycopg2
import os
from FineWatches.utils.choices import df

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    with conn.cursor() as cur:
        # Run users.sql
        with open('users.sql') as db_file:
            cur.execute(db_file.read())
        # Run produce.sql
        with open('watches.sql') as db_file:
            cur.execute(db_file.read())

        # Import all produce from the dataset
        all_watches = list(
            map(lambda x: tuple(x),
                df[['Brand', 'Model', 'Case Material', 'Strap Material',
                'Movement Type', 'Water Resistance', 'Case Diameter (mm)','Case Thickness (mm)',
                'Band Width (mm)', 'Dial Color', 'Crystal Material', 'Complications',
                'Power Reserve', 'Price (USD)']].to_records(index=False))
                )
        args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in all_watches)
        cur.execute("""
            INSERT INTO Watches (
                Brand, Model, "Case Material", "Strap Material", "Movement Type",
                "Water Resistance", "Case Diameter", "Case Thickness", "Band Width",
                "Dial Color", "Crystal Material", "Complications", "Power Reserve", Price
            )
            VALUES """ + args_str)
        # Dummy costumer 1 sells all watces
        dummy_sales = [(1, i) for i in range(1, len(all_watches) + 1)]
        args_str = ','.join(cur.mogrify("(%s, %s)", i).decode('utf-8') for i in dummy_sales)
        cur.execute("INSERT INTO Sell (brandrep_pk, watches_pk) VALUES " + args_str)

        conn.commit()

    conn.close()
