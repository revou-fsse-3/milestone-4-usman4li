from flask import Blueprint, jsonify, render_template, request
from connectors.mysql_connector import engine

from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/register", methods=['GET','POST'])
def do_register():
    if request.method == 'POST':

        try:
            data = request.get_json()
            username = data['name']
            email = data['email']
            password_hash = data['password_hash']

            print("name:", username)

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
                return jsonify({ "message": "Gagal Register" })

            return jsonify({ "message": "Sukses Register" })

        except Exception as e:
            print(e)
            return jsonify({ "message": "Internal Server Error" }), 500
    else:
        return render_template("user/register.html")

@user_routes.route("/login", methods=['GET','POST'])
def do_user_login():
    if request.method == 'POST':

        try:
            data = request.get_json()
            email = data['email']
            password_hash = data['password_hash']

            connection = engine.connect()
            Session = sessionmaker(connection)
            session = Session()

            users = session.query(User).filter(User.email==email).first()

            if users == None:
                return jsonify({"message": "Email tidak terdaftar"})
            
            #Check Password
            if not users.check_password(password_hash):
                return jsonify({"message" : "password Salah"})

            login_user(users, remember=False)
            return jsonify({ "message": "Login berhasil" }), 200
            
        except Exception as e:
            print(e)
            return jsonify({ "message": "Login Gagal" }), 500
    
    else:
        return render_template("user/login.html")
    
@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return jsonify({ "message": "Logout berhasil" }), 200