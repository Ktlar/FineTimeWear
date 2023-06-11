Before running this web app, there are couple of requirements which must be 
followed, these requirements are listed below:

1. Create a database in pgAdmin named "FineWatches".

2. Chance the db_user/password/name of the db_init.py and __init__.py so that it fits your computer, example:

SECRET_KEY='abracadabra23456134668'
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=FineWatches

3. Change directory to /utils/ and then type:
    "python db_init.py"
To fill your new database.

4. Install requirements with:

pip install -r requirements.txt

5. Replace the path in "choices.py" for the dataset with your own:

DATASET_PATH = 'C:/Users/oliko/OneDrive/Dokumenter/GitHub/FineTimeWear/FineWatches/dataset/Luxury watch.csv'

6. Now set directory to ".../FineTimeWear/FineWatches" and run:

    "python -m flask run"
    
 
