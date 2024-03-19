from flask import Blueprint, render_template, request, jsonify
from connectors.mysql_connector import Session, engine
from models.account import Account
from models.transaction import Transaction
from sqlalchemy import Engine, select
from sqlalchemy.orm import sessionmaker
from flask_login import current_user, login_required

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route("/transaction", methods=['GET'])
def transaction_list():
    response_data = dict()

    session = Session()

    try:
        transaction_query = select(Transaction)

        if request.args.get('query') is not None:
            search_query = request.args.get('query')
            transaction_query = transaction_query.where(Transaction.id.like(f'%{ search_query }%'))

        transaction = session.execute(transaction_query)
        transaction = transaction.scalars()
        response_data['transaction'] = transaction
        print(transaction)
    except Exception as e:
        print(e)
        return "Error"
    
    return render_template("transaction/transaction.html", response_data = response_data)

@transaction_routes.route("/transaction", methods=['POST'])
def make_transaction():
    response_data = dict()
    data = request.json

    # connect to database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    from_account = session.query(Account).filter_by(account_number=data['account_number']).first()
    to_account = session.query(Account).filter_by(account_number=data['account_number']).first()

    try:
        # Check jika account ada
        if from_account and to_account:

            if from_account.balance >= data['amount']:
                from_account.balance -= data['amount']
                to_account.balance += data['amount']

                # Buat transaksi
                new_transaction = Transaction(
                    from_account_id = data['from_account_id'],
                    to_account_id = data['to_account_id'],
                    amount = data['amount'],
                    type = data['type'],
                    description = data['description']
                )

                session.add(new_transaction)

                # update database
                session.commit()
                session.close()

                return jsonify({"message": "Transaction successful"}), 200
            
            else:
                return jsonify({"message": "Insufficient balance"}), 400
        
        else:
            return jsonify({"message": "One or both accounts not found"}), 404
        
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({"message": "Error processing transaction"}), 500
