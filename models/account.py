
from sqlalchemy import DECIMAL, DateTime, Integer, String, func
from models.base import Base
from sqlalchemy.orm import mapped_column

class Account(Base):
    __tablename__ = 'Accounts'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, nullable=False)   
    account_type = mapped_column(String(255), nullable=False)
    account_number = mapped_column(String(255), nullable=False)
    balance = mapped_column(DECIMAL(10,2), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())
 