from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_URL')
database = os.getenv('DB_NAME')

# URL koneksi MySQL
connection_url = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"

# mesin SQLAlchemy
engine = create_engine(connection_url)

# sessionmaker
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
