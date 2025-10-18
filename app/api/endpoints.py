from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.ml.model import FraudDetectionModel
from app.schemas import (
    TransactionCreate, TransactionResponse, FraudPrediction,
    BatchPredictionRequest, BatchPredictionResponse, HealthCheck
)
from app.models import Transaction

router = APIRouter()

# Dependency (will be overridden in main.py)
async def get_fraud_model():
    raise HTTPException(status_code=503, detail="Model not available")

@router.post("/predict", response_model=FraudPrediction)
async def predict_fraud(
    transaction: TransactionCreate,
    model: FraudDetectionModel = Depends(get_fraud_model),
    db: Session = Depends(get_db)
):
    """Predict fraud for a single transaction"""
    try:
        # Make prediction
        transaction_dict = transaction.dict()
        prediction = model.predict(transaction_dict)
        
        # Store in database
        db_transaction = Transaction(
            **transaction_dict,
            is_fraud=prediction["prediction"],
            fraud_probability=prediction["probability"],
            risk_level=prediction["risk_level"]
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        # Add transaction ID to response
        prediction["transaction_id"] = transaction.transaction_id
        
        return prediction
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch_fraud(
    batch_request: BatchPredictionRequest,
    model: FraudDetectionModel = Depends(get_fraud_model)
):
    """Predict fraud for multiple transactions"""
    try:
        transactions = [tx.dict() for tx in batch_request.transactions]
        results = model.predict_batch(transactions)
        
        # Add transaction IDs to results
        for i, result in enumerate(results):
            result["transaction_id"] = batch_request.transactions[i].transaction_id
        
        fraud_count = sum(1 for r in results if r["prediction"])
        fraud_rate = fraud_count / len(results) if results else 0
        
        return BatchPredictionResponse(
            results=results,
            total_transactions=len(results),
            fraud_count=fraud_count,
            fraud_rate=round(fraud_rate, 4)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@router.get("/health", response_model=HealthCheck)
async def health_check(model: FraudDetectionModel = Depends(get_fraud_model)):
    """Health check endpoint"""
    return HealthCheck(
        status="healthy" if model.is_loaded else "degraded",
        model_loaded=model.is_loaded,
        service="fraud-detection-api",
        timestamp=pd.Timestamp.now()
    )

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get recent transactions"""
    transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/model/info")
async def get_model_info(model: FraudDetectionModel = Depends(get_fraud_model)):
    """Get model information"""
    return {
        "version": model.model_version,
        "loaded": model.is_loaded,
        "type": "fraud-detection"
    }