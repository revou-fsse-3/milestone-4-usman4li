
import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from connectors.mysql_connector import engine
from controllers.user import user_routes
from controllers.transaction import transaction_routes
from controllers.account import account_routes
from models.user import User
from models.transaction import Transaction


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(user_routes)
app.register_blueprint(transaction_routes)
app.register_blueprint(account_routes)

# Product Route
@app.route("/")
def hello_world():
    # return "Sukses"

    # transaction_query = select(Transaction)
    # Session = sessionmaker(engine)
    # with Session() as session:
    #     result = session.execute(transaction_query)
    #     for row in result.scalars():
    #         print(f'ID: {row.id}, Name: {row.from_account_id}')
    # return redirect(url_for('user_routes.do_user_login'))
    return redirect('/account')
 