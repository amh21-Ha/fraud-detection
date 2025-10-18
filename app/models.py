from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, default=generate_uuid)
    transaction_id = Column(String(50), unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    timestamp = Column(DateTime, nullable=False)
    merchant_id = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    location = Column(String(100))
    country = Column(String(2), default="US")
    ip_address = Column(String(45))
    is_fraud = Column(Boolean, default=False)
    fraud_probability = Column(Float, default=0.0)
    risk_level = Column(String(20), default="low")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Transaction({self.transaction_id}, ${self.amount}, fraud: {self.is_fraud})>"