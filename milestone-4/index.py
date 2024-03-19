import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from connectors.mysql_connector import get_session
from controllers.user_CRUD import crud_routes
from controllers.account_CRUD import account_routes
from controllers.transaction_CRUD import transaction_routes
from models.user import User

load_dotenv()

app = Flask(__name__)

# Set secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = get_session()
    
    return session.query(User).get(int(user_id))

jwt = JWTManager(app)
# Register Blueprint untuk rute-rute CRUD pengguna
app.register_blueprint(crud_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)

@app.route('/')
def home():
    return "Sukses"

if __name__ == '__main__':
    app.run(debug=True)
