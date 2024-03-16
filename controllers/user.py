from flask import Blueprint, redirect, render_template, request
from connectors.mysql_connector import engine

from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user
user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/register", methods=['GET'])
def user_register():
    return render_template("user/register.html")

@user_routes.route("/register", methods=['POST'])
def do_register():
    username = request.form['username']
    email = request.form['email']
    password_hash = request.form['password_hash']

    NewUser = User(username=username, email=email)
    NewUser.set_password(password_hash)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(NewUser)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error during registration: {e}")
        return { "message": "Gagal Register" }

    return { "message": "Sukses Register" }

@user_routes.route("/login", methods=['GET'])
def user_login():
    return render_template("user/login.html")

@user_routes.route("/login", methods=['POST'])
def do_user_login():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        users = session.query(User).filter(User.email==request.form['email']).first()

        if users == None:
            return {"message": "Email tidak terdaftar"}
        
        #Check Password
        if not users.check_password(request.form['password_hash']):
            return {"message" : "password Salah"}

        login_user(users, remember=False)
        return redirect('/transactions')
    
    except Exception as e:
        print(e)
        return { "message": "Login Failed"}
    


@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return (redirect('/login'))