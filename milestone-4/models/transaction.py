from sqlalchemy import DECIMAL, DateTime, Integer, String, func
from models.base import Base
from sqlalchemy.orm import mapped_column

class Transaction(Base):
    __tablename__ = 'Transactions'

    id = mapped_column(Integer, primary_key=True, autoincrement=True) 
    from_account_id = mapped_column(Integer, nullable=False)
    to_account_id = mapped_column(Integer, nullable=False)
    amount = mapped_column(DECIMAL(10,2), nullable=False)
    type = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Transactions(id={self.id}, from_account_id={self.from_account_id}, to_account_id={self.to_account_id}, amount={self.amount}, type={self.type}, description={self.description}, created_at={self.created_at})>"
    