import bcrypt
from flask import Blueprint, redirect, request, jsonify, render_template, url_for, session as flask_session
from flask_jwt_extended import create_access_token
from flask_login import LoginManager, UserMixin, login_required, logout_user
from sqlalchemy import func
from models.account import Account
from models.user import User
from connectors.mysql_connector import get_session

crud_routes = Blueprint('crud_routes', __name__)

# # Create User (Registration)
# @crud_routes.route('/register', methods=['GET', 'POST'])
# def register_user():
#     if request.method == 'GET':
#         return render_template('register.html')
#     elif request.method == 'POST':
#         data = request.form
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password_hash')
#         account = data.get('account_type')

#         # create new user
#         NewUser = User(username=username, email=email)
#         NewUser.set_password(password)

#         # memanggil data dari database MySQL
#         session = get_session()
#         session.begin()
#         try:
#             #add new user ke database
#             session.add(NewUser)
#             session.flush()

#             account_number = session.query(Account).count() + 1000000
#             new_account = Account(user_id=NewUser.id, account_type=account, account_number=account_number)
#             session.add(new_account)
#             session.commit()
#             return jsonify({'message': 'User registered successfully'}), 201
    
#         except Exception as e:
#             print(e)
#             session.rollback()
#             return { "message": "Gagal Register" }  
        
# # User Login
# @crud_routes.route('/login', methods=['GET', 'POST'])
# def login_user():
#     if request.method == 'GET':
#         return render_template('login.html')
#     elif request.method == 'POST':
#         if request.is_json:
#             data = request.json
#             email = data.get('email')
#             password = data.get('password_hash')
#         else:
#             data = request.form
#             email = data.get('email')
#             password = data.get('password_hash')  # Menggunakan 'password' untuk mengambil password

#         print(email)
#         print(password)
#         session = get_session()
#         user = session.query(User).filter_by(email=email).first()
#         print(user)
#         if user:

#             if user.check_password(password):
#                   # Membandingkan password konversi hash yang dimasukkan dengan password yang ada di database
#                 print (user.check_password(password))
#                 return jsonify({'message': 'Login successful'}), 200
#             else:
#                 return jsonify({'message': 'Login failed. Incorrect password'}), 401
            
#         else:
#             return jsonify({'message': 'Login failed. Email not registered'}), 401

@crud_routes.route('/user/<int:id>', methods=['GET'])
def get_user_id(id):
    session = get_session()
    user = session.query(User).filter_by(id=id).first()
    session.close()

    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password_hash,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        return jsonify(user_data), 200
    
    else:
        return jsonify({'message': 'User not found'})
    

# @crud_routes.route('/user/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     session = get_session()
    
#     # Mengambil data pengguna berdasarkan ID
#     user = session.query(User).filter(User.id == id).first()

#     if not user:
#         return jsonify({'message': 'User not found'}), 404
    
#     else:
#         # Menghapus data pengguna dari database
#         session.delete(user)
#         session.commit()

#         # Mengembalikan respons berhasil
#         return jsonify({'message': 'Account deleted successfully'}), 204

@crud_routes.route('/register_page', methods=['GET'])
def register_user_page():
    return render_template('register.html')

@crud_routes.route('/register', methods=['POST'])
def register_user():
    data = request.form

    # Cek data request
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing {field} field'}), 400

    # Membuat instance User
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])

    # Menambahkan user baru ke dalam database
    session = get_session()
    session.add(new_user)
    session.commit()

    # Simpan user_id di sesi Flask
    flask_session['user_id'] = new_user.id

    # Render halaman register-logout.html dengan nama pengguna yang berhasil registrasi
    return render_template('register-logout.html', username=new_user.username)


# Metode Logout
@crud_routes.route('/logout_page', methods=['GET'])
def logout_page_login():
    return render_template('login-logout.html')

@crud_routes.route('/logout_page', methods=['GET'])
def logout_page_register():
    return render_template('register-logout.html')

@crud_routes.route('/logout', methods=['GET'])
def logout():
    # Hapus user_id dari sesi Flask
    flask_session.pop('user_id', None)
    # Memberikan respons bahwa logout berhasil
    return jsonify({'message': 'Logout berhasil'}), 200

@crud_routes.route('/login_page', methods=['GET'])
def login_page():
    return render_template('login.html')

@crud_routes.route('/login', methods=['POST'])
def login():
    data = request.form

    # Cek keberadaan data yang dibutuhkan
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing {field} field'}), 400

    # Mendapatkan session database
    session = get_session()

    username = data['username']
    # Mengambil user berdasarkan username
    user = session.query(User).filter(User.username == username).first()

    # Periksa apakah pengguna ditemukan dan password cocok
    if user and user.check_password(data['password']):
        # Redirect ke halaman yang mirip dengan halaman logout
        return render_template('login-logout.html', username=data['username']), 200
    else:
        return jsonify({'message': 'Username atau password salah'}), 401


@crud_routes.route('/update_page')
def update_page():
    return render_template('update_user.html')
@crud_routes.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    # Dapatkan data yang dikirim dalam permintaan
    data = request.json

    # Dapatkan sesi database
    session = get_session()

    # Dapatkan pengguna yang sedang login
    current_user = session.query(User).filter(User.id == id).first()

    # Verifikasi keberadaan pengguna dan sesi yang aktif
    if not current_user:
        return jsonify({'message': 'User not found'}), 404

    # Verifikasi sesi pengguna sebelum memperbarui profilnya
    if 'user_id' not in session or session['user_id'] != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 401

    # Perbarui data pengguna
    if 'new_username' in data:
        current_user.username = data['new_username']
    if 'new_email' in data:
        current_user.email = data['new_email']
    if 'new_password' in data:
        current_user.set_password(data['new_password'])

    # Komit perubahan ke database
    session.commit()

    return jsonify({'message': 'User profile updated successfully'}), 200

@crud_routes.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    # Mendapatkan session database
    session = get_session()

    # Mengambil pengguna berdasarkan ID
    user = session.query(User).filter(User.id == id).first()

    if user:
        # Mengonversi objek pengguna menjadi format yang dapat di-JSON-kan
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404