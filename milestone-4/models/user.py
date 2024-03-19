from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import bcrypt

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Set user's password and store its hash."""
        # Hash the password and convert it to a string
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the one stored in the database."""
        # Check if the password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True  # Or implement logic as needed

    def is_authenticated(self):
        # Implement your logic here, for example:
        return True  # Assuming all users are authenticated by default

    def is_anonymous(self):
        return False
