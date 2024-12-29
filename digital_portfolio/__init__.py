from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
# >>> import secrets
# >>> secrets.token_hex(16)
# 'd84d5540915408f9f2a942d2fcc5da75'
app.config['SECRET_KEY'] = 'd84d5540915408f9f2a942d2fcc5da75'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from digital_portfolio.users.routes import users
from digital_portfolio.portfolio.routes import portfolio
from digital_portfolio.main.routes import main

app.register_blueprint(users)
app.register_blueprint(portfolio)
app.register_blueprint(main)