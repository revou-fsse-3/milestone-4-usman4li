
from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker

from connectors.mysql_connector import engine
from models.account import Account

# account routes blueprint
account_routes = Blueprint('account_routes', __name__)

@account_routes.route("/account", methods=['GET'])
def account_list():
    response_data = dict()

    # connect to database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        account_query = select(Account)

        if request.args.get('query') is not None:
            search_query = request.args.get('query')
            account_query = account_query.where(Account.user_id.like(f'%{ search_query }%'))

        account = session.execute(account_query)
        account = account.scalars()
        response_data['account'] = account
        print(account)
    except Exception as e:
        print(e)
        return "Error"
    
    return render_template("account/account.html", response_data = response_data)

@account_routes.route("/account", methods=['POST'])
def add_account():
    response_data = dict()
    data = request.json

    # connect to database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    existing_account = session.query(Account).filter_by(account_number=data['account_number']).first()

    try:
        if existing_account:
            # check account type
            if existing_account.account_type == 'savings':
                # savings / mengubah request menjadi PUT
                return add_account_to_update_account(existing_account.id, data)
                # existing_account.balance += data['balance']
                # session.commit()
                # session.close()
                # response_data['message'] = "Account balance updated successfully."
                # return jsonify(response_data), 200
            else:
                # checking
                last_balance = existing_account.balance
                session.close()
                response_data['message'] = f"Cannot add balance to non-savings account type. Last balance: {last_balance}"
                return jsonify(response_data), 400

        else:
            new_account = Account(
                user_id = data['user_id'],
                account_type = data['account_type'],
                account_number = data['account_number'],
                balance=data['balance']
            )
            session.add(new_account)
            session.commit()
            session.close()
            response_data['message'] = "Account added successfully."
            return jsonify(response_data), 201

    except Exception as e:
        session.rollback()
        session.close()
        return { "message": "Account added failed"}

def add_account_to_update_account(account_id, data):
    response_data = dict()
    # connect to database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        existing_account = session.query(Account).get(account_id)
        if existing_account:
            existing_account.balance += data['balance']
            session.commit()
            session.close()
            response_data['message'] = "Account balance updated successfully."
            return jsonify(response_data), 200
        else:
            session.close()
            response_data['message'] = "Account not found."
            return jsonify(response_data), 404
    except Exception as e:
        session.rollback()
        session.close()
        return { "message": "Account update failed"}

@account_routes.route("/account/<int:id>", methods=['PUT'])
def edit_account(id):
    response_data = dict()
    data = request.json

    # connect to database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        # Retrieve account by ID
        account = session.query(Account).filter_by(id=id).first()

        if account:
            # Update account balance
            account.balance = data['balance']
            session.commit()
            session.close()
            response_data['message'] = "Account balance updated successfully."
            return jsonify(response_data), 200
        
        else:
            session.close()
            response_data['message'] = "Account not found."
            return jsonify(response_data), 404
        
    except Exception as e:
        session.rollback()
        session.close()
        return { "message": "Failed to update account balance."}, 500

@account_routes.route("/account/<int:id>", methods=['DELETE'])
def delete_account(id):
    response_data = {}

    # connect to database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        # Query the account
        account = session.query(Account).get(id)
        if account:
            session.delete(account)
            session.commit()
            response_data['message'] = f"Account with ID {id} deleted successfully."
            return jsonify(response_data), 200
        else:
            response_data['message'] = f"Account with ID {id} not found."
            return jsonify(response_data), 404
    except Exception as e:
        session.rollback()
        response_data['message'] = f"Failed to delete account with ID {id}."
        return jsonify(response_data), 500
    finally:
        session.close()