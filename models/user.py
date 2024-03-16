import bcrypt
from sqlalchemy import DateTime, Integer, String, func
from models.base import Base
from sqlalchemy.orm import mapped_column

from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = 'Users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255), nullable=False)   
    email = mapped_column(String(255), nullable=False)
    password_hash = mapped_column(String(255))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.name}>'


    def set_password(self, password_hash):
        self.password_hash = bcrypt.hashpw(password_hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password_hash):
        return bcrypt.checkpw(password_hash.encode('utf-8'), self.password_hash.encode('utf-8'))