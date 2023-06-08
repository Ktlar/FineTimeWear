Before running this web app, there are couple of requirements which must be 
followed, these requirements are listed below:

1. Create a database in pgAdmin named "FineWatches".

2. Chance the contents of the .env so that it fits your computer, example:

SECRET_KEY=b'\x1f\xb9_Q\xfb&\x8f\x0bD\xcf\xdbr\xac\x0f6CN\xc8\xc8\xa3\xfa)\xbem\xc9P\xd8?\xcd\xc8!0'
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=FineWatches

3. Install requirements with:

pip install -r requirements.txt

4. Replace the path in "choices.py" for the dataset with your own:

DATASET_PATH = 'C:/Users/oliko/OneDrive/Dokumenter/GitHub/FineTimeWear/FineWatches/dataset/Luxury watch.csv'
 
