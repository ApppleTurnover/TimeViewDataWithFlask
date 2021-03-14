from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from parserdata.config import Test


app = Flask(__name__)
app.config.from_object(Test)

login_manager = LoginManager()
login_manager.init_app(app)

Bootstrap(app)

db = SQLAlchemy(app)

