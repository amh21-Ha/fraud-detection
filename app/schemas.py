from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Base schema with the fix
class BaseSchema(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

class TransactionBase(BaseSchema):
    transaction_id: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    timestamp: datetime
    merchant_id: str = Field(..., min_length=1, max_length=50)
    customer_id: str = Field(..., min_length=1, max_length=50)
    currency: str = Field(default="USD")
    location: Optional[str] = None
    country: Optional[str] = None

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

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

class FraudPrediction(BaseSchema):
    transaction_id: str
    prediction: bool
    probability: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    model_version: str
    features_used: List[str]

class BatchPredictionRequest(BaseSchema):
    transactions: List[TransactionCreate]

class BatchPredictionResponse(BaseSchema):
    results: List[FraudPrediction]
    total_transactions: int
    fraud_count: int
    fraud_rate: float

class HealthCheck(BaseSchema):
    status: str
    model_loaded: bool
    service: str
    timestamp: datetime

class ModelInfo(BaseSchema):
    version: str
    features: List[str]
    performance: Dict[str, float]
    training_date: str