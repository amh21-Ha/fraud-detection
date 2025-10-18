from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TransactionBase(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    timestamp: datetime
    merchant_id: str = Field(..., min_length=1, max_length=50)
    customer_id: str = Field(..., min_length=1, max_length=50)
    currency: str = Field(default="USD")
    location: Optional[str] = None
    country: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    uuid: str
    is_fraud: bool
    fraud_probability: float
    risk_level: RiskLevel
    created_at: datetime

    class Config:
        from_attributes = True

class FraudPrediction(BaseModel):
    transaction_id: str
    prediction: bool
    probability: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    model_version: str

class BatchPredictionRequest(BaseModel):
    transactions: List[TransactionCreate]

class BatchPredictionResponse(BaseModel):
    results: List[FraudPrediction]
    total_transactions: int
    fraud_count: int
    fraud_rate: float

class HealthCheck(BaseModel):
    status: str
    model_loaded: bool
    service: str
    timestamp: datetime