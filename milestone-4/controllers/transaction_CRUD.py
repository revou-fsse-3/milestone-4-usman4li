from decimal import Decimal
from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import TIMESTAMP
from models.transaction import Transaction
from models.account import Account
from connectors.mysql_connector import get_session
from datetime import datetime

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route('/transactions_page', methods=['GET'])
def login_page():
    return render_template('transaction.html')
from decimal import Decimal

@transaction_routes.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.json

    required_fields = ['from_account_number', 'to_account_number', 'amount', 'type', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing {field} field'}), 400
    
    data['amount'] = Decimal(data['amount'])

    # Mendapatkan sesi database
    session = get_session()
    try:
        # Mendapatkan akun pengirim dan penerima berdasarkan nomor akun
        from_account = session.query(Account).filter_by(account_number=data['from_account_number']).first()
        to_account = session.query(Account).filter_by(account_number=data['to_account_number']).first()

        # Memeriksa apakah akun pengirim dan penerima ditemukan
        if not from_account or not to_account:
            return jsonify({'message': 'One or both of the accounts not found'}), 404

        # Memeriksa saldo cukup untuk melakukan transaksi
        if from_account.balance < data['amount']:
            return jsonify({'message': 'Insufficient balance for transaction'}), 400

        # Membuat objek transaksi baru
        new_transaction = Transaction(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=data['amount'],
            type=data['type'],
            description=data['description']
        )

        # Menambahkan transaksi baru ke dalam database
        session.add(new_transaction)

        # Update saldo akun pengirim dan penerima
        from_account.balance -= data['amount']
        to_account.balance += data['amount']

        # Commit perubahan ke dalam database
        session.commit()

        return jsonify({'message': 'Transaction successful'}), 201

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        session.rollback()  # Menggulirkan kembali transaksi jika terjadi kesalahan
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()


@transaction_routes.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    # Mendapatkan sesi database
    session = get_session()

    try:
        # Mendapatkan transaksi berdasarkan ID
        transaction = session.query(Transaction).get(id)

        # Memeriksa apakah transaksi ditemukan
        if not transaction:
            return jsonify({'message': 'Transaction not found'}), 404

        # Menghapus transaksi dari database
        session.delete(transaction)
        session.commit()

        return jsonify({'message': 'Transaction deleted successfully'}), 200

    except Exception as e:
        session.rollback()  # Menggulirkan kembali transaksi jika terjadi kesalahan
        return jsonify({'message': str(e)}), 500

    finally:
        session.close()

@transaction_routes.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        session = get_session()  # Get the database session
        transactions = session.query(Transaction).all()  # Get all transactions from the database
        # Convert the list of transactions to JSON format
        transactions_json = []
        for transaction in transactions:
            transaction_data = {
                'id': transaction.id,
                'from_account_id': transaction.from_account_id,
                'to_account_id': transaction.to_account_id,
                'amount': str(transaction.amount),
                'type': transaction.type,
                'description': transaction.description,
                'timestamp': transaction.created_at
            }
            transactions_json.append(transaction_data)

        # Return the list of transactions in JSON format
        return jsonify(transactions_json), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@transaction_routes.route('/transactions/<int:id>', methods=['GET'])
def get_transaction_by_id(id):
    try:
        session = get_session()  # import database
        transaction = session.query(Transaction).filter_by(id=id).first()  # Ambil transaksi berdasarkan ID
        if not transaction:
            return jsonify({'message': 'Transaction not found'}), 404  # Kembalikan pesan jika transaksi tidak ditemukan
        
        # Ubah objek transaksi menjadi format JSON
        transaction_data = {
            'id': transaction.id,
            'from_account_id': transaction.from_account_id,
            'to_account_id': transaction.to_account_id,
            'amount': str(transaction.amount),
            'type': transaction.type,
            'description': transaction.description,
            'created_at': transaction.created_at
        }

        return jsonify(transaction_data), 200  # Kembalikan data transaksi dalam format JSON

    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Kembalikan pesan kesalahan jika terjadi kesalahan

    finally:
        session.close()