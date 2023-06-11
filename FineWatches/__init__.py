import psycopg2
from flask import Flask
from flask_login import LoginManager
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config['SECRET_KEY'] = "abracadabra23456134668"

conn = psycopg2.connect(
    host="localhost",
    database="FineWatches",
    user="postgres",
    password="eplavelta"
)

db_cursor = conn.cursor(cursor_factory=RealDictCursor)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from FineWatches import filters
from FineWatches.blueprints.Login.routes import Login
from FineWatches.blueprints.Watches.routes import Watch

app.register_blueprint(Login)
app.register_blueprint(Watch)
