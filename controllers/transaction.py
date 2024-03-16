from flask import Blueprint, render_template, request, jsonify
from connectors.mysql_connector import Session
from models.transaction import Transaction
from sqlalchemy import Engine, select
from sqlalchemy.orm import sessionmaker
from flask_login import current_user, login_required

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route("/transaction", methods=['GET'])
def transaction_list():
    response_data = dict()

    # connect to database
    # connection = Engine.connect()
    # Session = sessionmaker(connection)
    session = Session()

    try:
        transaction_query = select(Transaction)

        if request.args.get('query') is not None:
            search_query = request.args.get('query')
            trancation_query = transaction_query.where(Transaction.user_id.like(f'%{ search_query }%'))

        transaction = session.execute(transaction_query)
        transaction = transaction.scalars()
        response_data['transaction'] = transaction
        print(transaction)
    except Exception as e:
        print(e)
        return "Error"
    
    return render_template("transaction/transaction.html", response_data = response_data)
