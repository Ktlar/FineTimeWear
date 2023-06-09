"""The __init__.py file seems to be the initialization file for the Flask application in the 
GreenGroceries module. Let's break down its contents:

Import Statements:

os: Allows access to various operating system functionalities.
psycopg2: A PostgreSQL adapter for Python that provides database connectivity.
dotenv: A library for reading variables from .env files into the environment.
Flask: The main Flask class used to create a Flask application.
LoginManager: A Flask extension for managing user authentication and sessions.
RealDictCursor: A cursor class from psycopg2.extras that returns rows as dictionaries instead of tuples.
Environment Configuration:

load_dotenv(): Loads the environment variables from the .env file into the application's environment.
Flask Application Initialization:

app = Flask(__name__): Creates a Flask application instance.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY'): Sets the secret key for the Flask application, retrieved from the environment variable SECRET_KEY.
Database Connection:

conn = psycopg2.connect(...): Establishes a connection to the PostgreSQL database using the provided connection parameters from the environment variables.
db_cursor = conn.cursor(cursor_factory=RealDictCursor): Creates a cursor object using RealDictCursor to fetch results as dictionaries.
LoginManager Configuration:

login_manager = LoginManager(app): Initializes the LoginManager extension with the Flask application.
login_manager.login_view = 'login': Sets the login view to the endpoint named 'login'.
login_manager.login_message_category = 'info': Sets the category for login messages to 'info'.
Blueprint and Route Registration:

from GreenGroceries import filters: Imports the custom template filters from the filters module.
from GreenGroceries.blueprints.Login.routes import Login: Imports the login blueprint and its routes.
from GreenGroceries.blueprints.Produce.routes import Produce: Imports the produce blueprint and its routes.
app.register_blueprint(Login): Registers the login blueprint with the Flask application.
app.register_blueprint(Produce): Registers the produce blueprint with the Flask application.
This __init__.py file sets up the Flask application, configures the database connection, 
initializes the login manager, and registers the blueprints and routes for the application. 
It provides the foundation for running the GreenGroceries web application """
"""The __init__.py file seems to be the initialization file for the Flask application in the 
GreenGroceries module. Let's break down its contents:

Import Statements:

os: Allows access to various operating system functionalities.
psycopg2: A PostgreSQL adapter for Python that provides database connectivity.
dotenv: A library for reading variables from .env files into the environment.
Flask: The main Flask class used to create a Flask application.
LoginManager: A Flask extension for managing user authentication and sessions.
RealDictCursor: A cursor class from psycopg2.extras that returns rows as dictionaries instead of tuples.
Environment Configuration:

load_dotenv(): Loads the environment variables from the .env file into the application's environment.
Flask Application Initialization:

app = Flask(__name__): Creates a Flask application instance.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY'): Sets the secret key for the Flask application, retrieved from the environment variable SECRET_KEY.
Database Connection:

conn = psycopg2.connect(...): Establishes a connection to the PostgreSQL database using the provided connection parameters from the environment variables.
db_cursor = conn.cursor(cursor_factory=RealDictCursor): Creates a cursor object using RealDictCursor to fetch results as dictionaries.
LoginManager Configuration:

login_manager = LoginManager(app): Initializes the LoginManager extension with the Flask application.
login_manager.login_view = 'login': Sets the login view to the endpoint named 'login'.
login_manager.login_message_category = 'info': Sets the category for login messages to 'info'.
Blueprint and Route Registration:

from GreenGroceries import filters: Imports the custom template filters from the filters module.
from GreenGroceries.blueprints.Login.routes import Login: Imports the login blueprint and its routes.
from GreenGroceries.blueprints.Produce.routes import Produce: Imports the produce blueprint and its routes.
app.register_blueprint(Login): Registers the login blueprint with the Flask application.
app.register_blueprint(Produce): Registers the produce blueprint with the Flask application.
This __init__.py file sets up the Flask application, configures the database connection, 
initializes the login manager, and registers the blueprints and routes for the application. 
It provides the foundation for running the GreenGroceries web application """
import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from psycopg2.extras import RealDictCursor

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = psycopg2.connect(
    host="localhost",
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD')
)

db_cursor = conn.cursor(cursor_factory=RealDictCursor)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from FineWatches import filters
from FineWatches.blueprints.Login.routes import Login
from Finewatches.blueprints.Watches.routes import Watches

app.register_blueprint(Login)
app.register_blueprint(Watches)
