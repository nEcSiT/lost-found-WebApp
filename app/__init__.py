
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv

# Load environment variables from .env (local dev)
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
mail = Mail(app)

from . import routes, models, auth, api
app.register_blueprint(api.api)
