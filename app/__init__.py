from flask import Flask
from flask_mail import Mail # type: ignore[import-untyped]
from config import Config
from flask_migrate import Migrate # type: ignore[import-untyped]
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)
jwt = JWTManager(app)

from app import models
from app import routes