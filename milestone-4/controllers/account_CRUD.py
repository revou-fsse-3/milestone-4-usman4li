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