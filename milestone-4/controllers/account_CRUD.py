# from sqlite3 import IntegrityError
# from flask import Blueprint, abort, jsonify, render_template, request, session as flask_session
# from flask_login import current_user, login_required
# from datetime import datetime

# from sqlalchemy import desc

# from connectors.mysql_connector import get_session
# from models.account import Account
# from models.transaction import Transaction
# from models.user import User


# account_routes = Blueprint('account_routes', __name__)


# @account_routes.route('/accounts', methods=['POST'])
# def create_bank_account():
#     if 'user_id' not in flask_session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     # Mendapatkan data dari body request
#     data = request.form

#     # Mendapatkan session database
#     session = get_session()

#     try:
#         # Membuat objek Account bank baru
#         new_account = Account(
#             user_id=flask_session['user_id'],
#             account_type=data['account_type'],
#             account_number=data['account_number'],
#             balance=data['balance']
#         )

#         # Menyimpan objek Account baru ke dalam database
#         session.add(new_account)
#         session.commit()

#         return jsonify({'message': 'Bank account created successfully'}), 201

#     except Exception as e:
#         # Mengembalikan pesan error jika terjadi kesalahan
#         return jsonify({'message': str(e)}), 500

# @account_routes.route('/accounts_page', methods=['GET'])
# def create_bank_account_page():

#     if 'user_id' not in flask_session:
#         return jsonify({'message': 'Unauthorized'}), 401
    
#     return render_template('account.html')


# # @account_routes.route('/accounts', methods=['GET'])
# # @login_required
# # def get_accounts_list():
# #     # Cek admin
# #     if current_user.role != 'Admin':
# #         abort(403)  # Forbidden jika bukan admin

# #     session = get_session()
# #     accounts = session.query(Account).all()
# #     session.close()

# #     # Format data akun
# #     accounts_list = []
# #     for account in accounts:
# #         account_data = {
# #             'id': account.id,
# #             'user_id': account.user_id,
# #             'account_type': account.account_type,
# #             'account_number': account.account_number,
# #             'balance': account.balance,
# #             'created_at': str(account.created_at),  # Konversi ke string
# #             'updated_at': str(account.updated_at)   # Konversi ke string
# #             # Tambahkan kolom lainnya sesuai kebutuhan
# #         }
# #         accounts_list.append(account_data)
# #         print(accounts_list)
# #     # Ubah ke format JSON dan kembalikan sebagai respons
# #     return jsonify({'accounts': accounts_list}), 200

# # liat list Account di database all
# @account_routes.route('/accounts', methods=['GET'])
# def get_all_accounts():
#     # Mendapatkan session database
#     session_db = get_session()

#     try:
#         # Mengambil semua akun bank dari database
#         all_accounts = session_db.query(Account).all()

#         # Membuat list untuk menyimpan data akun bank
#         accounts_data = []

#         # Mengonversi objek akun bank menjadi format yang dapat dijsonifikasi
#         for account in all_accounts:
#             account_data = {
#                 'id': account.id,
#                 'user_id': account.user_id,
#                 'account_type': account.account_type,
#                 'account_number': account.account_number,
#                 'balance': str(account.balance),
#                 'created_at': datetime.strftime(account.created_at, '%Y-%m-%d %H:%M:%S'),
#                 'updated_at': datetime.strftime(account.updated_at, '%Y-%m-%d %H:%M:%S')
#             }
#             accounts_data.append(account_data)

#         # Cek jika permintaan ingin format HTML
#         if request.accept_mimetypes.accept_html:
#             return render_template('list_accounts.html', accounts=accounts_data)
#         # Jika tidak, kembalikan respons JSON
#         return jsonify(accounts_data), 200

#     except Exception as e:
#         # Mengembalikan pesan error jika terjadi kesalahan
#         return jsonify({'message': str(e)}), 500

#     finally:
#         # Tutup sesi database
#         session_db.close()

# #liat account di database berdasarkan id
# @account_routes.route('/accounts/<int:user_id>', methods=['GET'])
# def get_accounts(user_id):
#     session = get_session()

#     try:
#         user = session.query(User).filter_by(id=user_id).first()
#         if not user:
#             session.close()
#             return jsonify({'message': 'User not found'}), 404
        
#         # Get user's bank accounts
#         user_accounts = session.query(Account).filter_by(user_id=user_id).all()
#         if not user_accounts:
#             session.close()
#             return jsonify({'message': 'User has no bank accounts yet'}), 404
        
#         accounts_data = []
#         for account in user_accounts:
#             # Get transaction history for the account
#             transactions = session.query(Transaction).filter_by(from_account_id=account.id).order_by(desc(Transaction.created_at)).all()
            
#             # Calculate balance based on transaction history
#             balance = account.balance
#             for transaction in transactions:
#                 if transaction.type == 'debit':
#                     balance -= transaction.amount
#                 elif transaction.type == 'credit':
#                     balance += transaction.amount
            
#             # Append account data with balance changes to the accounts_data list
#             account_data = {
#                 'id': account.id,
#                 'user_id': account.user_id,
#                 'account_type': account.account_type,
#                 'account_number': account.account_number,
#                 'balance': str(balance),
#                 'created_at': datetime.strftime(account.created_at, '%Y-%m-%d %H:%M:%S'),
#                 'updated_at': datetime.strftime(account.updated_at, '%Y-%m-%d %H:%M:%S')
#             }
#             accounts_data.append(account_data)

#         session.close()
#         return render_template('list_accounts.html', accounts=accounts_data)
#     except Exception as e:
#         session.close()
#         return jsonify({'message': str(e)}), 500

# #update account
# @account_routes.route('/accounts/<int:user_id>', methods=['PUT'])
# def update_user_account(user_id):
#     # Mendapatkan data dari body request
#     data = request.json

#     # Mendapatkan session database
#     session = get_session()

#     try:
#         # Memperbarui detail pengguna (Users)
#         user = session.query(User).filter_by(id=user_id).first()
#         if not user:
#             return jsonify({'message': 'User not found'}), 404
#         if 'username' in data:
#             user.username = data['username']
#         if 'email' in data:
#             user.email = data['email']
#         session.commit()

#         # Memperbarui detail akun bank (Account)
#         account = session.query(Account).filter_by(user_id=user_id).first()
#         if not account:
#             return jsonify({'message': 'User has no bank account yet'}), 404
#         if 'account_number' in data:
#             account.account_number = data['account_number']
#         if 'balance' in data:
#             account.balance = data['balance']
#         session.commit()

#         return jsonify({'message': 'User and account details updated successfully'}), 200

#     except Exception as e:
#         # Mengembalikan pesan error jika terjadi kesalahan
#         session.rollback()
#         return jsonify({'message': str(e)}), 500

#     finally:
#         # Tutup sesi database
#         session.close()

# # membuat account darurat
# @account_routes.route('/accounts', methods=['POST'])
# def create_bank_account_E():
#     # Mendapatkan data dari body request
#     data = request.json

#     # Mendapatkan session database
#     session = get_session()

#     try:
#         # Periksa apakah pengguna sudah memiliki akun bank
#         existing_account = session.query(Account).filter_by(user_id=data['user_id']).first()
#         if existing_account:
#             return jsonify({'message': 'User already has a bank account'}), 400

#         # Membuat objek Account bank baru
#         new_account = Account(
#             user_id=data['user_id'],
#             account_type=data['account_type'],
#             account_number=data['account_number'],
#             balance=data['balance']
#         )

#         # Menyimpan objek Account baru ke dalam database
#         session.add(new_account)
#         session.commit()

#         return jsonify({'message': 'Bank account created successfully'}), 201

#     except IntegrityError:
#         session.rollback()
#         return jsonify({'message': 'User not found'}), 404

#     except Exception as e:
#         # Mengembalikan pesan error jika terjadi kesalahan
#         return jsonify({'message': str(e)}), 500

# @account_routes.route('/Accounts/<int:id>', methods=['DELETE'])
# def delete_account(id):
#     session = get_session()
    
#     # Mengambil data akun berdasarkan ID
#     account = session.query(Account).filter(Account.id == id).first()

#     if not account:
#         return jsonify({'message': 'Account not found'}), 404
    
#     else:
#         # Menghapus data akun dari database
#         session.delete(account)
#         session.commit()

#         # Mengembalikan respons berhasil
#         return jsonify({'message': 'Account deleted successfully'}), 204

from functools import wraps
from flask import Blueprint, render_template, request, jsonify, session as flask_session
from sqlalchemy import func
from models.account import Account
from models.user import User
from connectors.mysql_connector import get_session
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user, login_required
from models.account import Account
from flask_sqlalchemy import SQLAlchemy

account_routes = Blueprint('account_routes', __name__)

@account_routes.route('/accounts_page', methods=['GET'])
def account_page():
    return render_template('account.html')
@account_routes.route('/accounts', methods=['POST'])
def create_account():
    # Ambil data pengguna yang sedang login
    user_id = flask_session.get('user_id')
    
    # Periksa apakah pengguna sudah login
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    # Dapatkan sesi database
    session = get_session()

    # Periksa apakah pengguna sudah memiliki akun
    existing_account = session.query(Account).filter_by(user_id=user_id).first()
    if existing_account:
        return jsonify({'message': 'User already has an account'}), 400

    # Tentukan jenis akun berdasarkan urutan pengguna yang membuat akun
    num_existing_accounts = session.query(Account).count()
    if num_existing_accounts == 0:
        account_type = 'platinum'
    elif num_existing_accounts == 1:
        account_type = 'gold'
    else:
        account_type = 'silver'

    # Dapatkan nomor akun dengan increment dari 100000
    last_account_number = session.query(func.max(Account.account_number)).scalar() or 99999
    account_number = str(int(last_account_number) + 1)

    # Buat objek Akun baru
    new_account = Account(user_id=user_id, account_type=account_type, account_number=account_number)

    # Tambahkan akun baru ke database
    session.add(new_account)
    session.commit()

    return jsonify({'message': 'Account created successfully'}), 201


@account_routes.route('/account/update/<int:id>', methods=['GET'])
@login_required
def update_account_page(id):
    # Pengguna telah login
    # Lanjutkan dengan logika tampilan

    # Anda bisa menggunakan render_template untuk mengirimkan ID pengguna ke halaman HTML
    return render_template('update_account.html', user_id=id)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if hasattr(current_user, 'id'):
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'User not logged in'}), 401
    return decorated_function

@login_required
@account_routes.route('/account/<int:id>', methods=['PUT'])
def update_account(id):
    session=get_session()
    # Pastikan pengguna telah login
    # Periksa apakah akun yang akan diupdate milik pengguna yang sedang login
    account = session.query(Account).filter_by(id=id, user_id=current_user.id).first()
    
    if account:
        # Lakukan proses update sesuai dengan data yang diterima dari form
        data = request.form
        
        try:
            # Update saldo jika nilai balance baru diberikan
            if 'balance' in data:
                new_balance = float(data['balance'])
                Account.balance += new_balance

            # Update jenis akun jika accountType baru diberikan
            if 'accountType' in data:
                new_type = data['accountType']
                if new_type in ['gold', 'platinum']:
                    Account.account_type = new_type
                else:
                    return jsonify({'message': 'Invalid account type. Allowed types: gold, platinum'}), 400

            # Commit perubahan ke database
            session.commit()

            return jsonify({'message': 'Account updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        # Jika akun tidak ditemukan atau bukan milik pengguna yang sedang login, kembalikan pesan error
        return jsonify({'message': 'Unauthorized access or account not found'}), 401
    
@account_routes.route('/account/<int:id>', methods=['DELETE'])
def delete_account(id):
    try:
        session = get_session()
        # Temukan akun berdasarkan ID
        account = session.query(Account).get(id)
        if account:
            # Hapus akun dari database
            session.delete(account)
            session.commit()
            return jsonify({'message': 'Account deleted successfully'}), 200
        else:
            return jsonify({'message': 'Account not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@account_routes.route('/accounts', methods=['GET'])
def get_accounts():
    try:
        session = get_session()
        # Ambil semua akun dari database
        accounts = session.query(Account).all()

        # Siapkan daftar untuk menyimpan data akun
        account_list = []
        for account in accounts:
            # Tambahkan detail akun ke dalam daftar
            account_list.append({
                'id': account.id,
                'user_id': account.user_id,
                'balance': account.balance,
                'account_type': account.account_type
            })

        # Return daftar akun dalam format JSON
        return jsonify({'accounts': account_list}), 200
    except Exception as e:
        # Jika terjadi kesalahan, kembalikan pesan kesalahan
        return jsonify({'message': str(e)}), 500

@account_routes.route('/account/<int:id>', methods=['GET'])
def get_account_by_id(id):
    try:
        session = get_session()
        # Cari akun berdasarkan ID
        account = session.query(Account).filter_by(id=id).first()

        if account:
            # Jika akun ditemukan, kembalikan detailnya dalam format JSON
            return jsonify({
                'id': account.id,
                'user_id': account.user_id,
                'balance': account.balance,
                'account_type': account.account_type
            }), 200
        else:
            # Jika akun tidak ditemukan, kembalikan pesan bahwa akun tidak ditemukan
            return jsonify({'message': 'Account not found'}), 404
    except Exception as e:
        # Jika terjadi kesalahan, kembalikan pesan kesalahan
        return jsonify({'message': str(e)}), 500