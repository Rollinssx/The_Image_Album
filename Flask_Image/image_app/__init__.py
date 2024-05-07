from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from image_app.forms import LoginForm, RegistrationForm
from flask_login import LoginManager



password = 'password123'
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())


app = Flask(__name__)

app.config['SECRET_KEY'] = hashed_password
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'  # Specify the login view for unauthorized users
login_manager.init_app(app)


app.app_context().push()
db.create_all()
