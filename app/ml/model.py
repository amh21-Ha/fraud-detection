import pandas as pd
import numpy as np
from typing import Dict, Any
import logging
import sqlite3
import json

logger = logging.getLogger(__name__)

class FraudDetectionModel:
    """Ultra-light fraud detection without scikit-learn"""
    
    def __init__(self):
        self.is_loaded = True  # Always available
        self.model_version = "1.0.0-light"
    
    def load_model(self, model_path: str):
        """No actual model loading needed"""
        logger.info("✅ Using rule-based fraud detection")
    
    def predict(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based fraud detection (no ML dependencies)"""
        try:
            amount = transaction_data.get('amount', 0)
            timestamp = pd.to_datetime(transaction_data.get('timestamp'))
            hour = timestamp.hour
            
            # Simple rule-based scoring
            fraud_score = 0
            
            # Rule 1: Large amounts
            if amount > 5000:
                fraud_score += 3
            elif amount > 2000:
                fraud_score += 2
            elif amount > 1000:
                fraud_score += 1
            
            # Rule 2: Unusual hours (1AM-5AM)
            if 1 <= hour <= 5:
                fraud_score += 2
            
            # Rule 3: Very small amounts (potential test transactions)
            if amount < 1:
                fraud_score += 2
            
            # Rule 4: Round numbers (potential test)
            if amount % 100 == 0 and amount > 100:
                fraud_score += 1
            
            # Convert to probability (0 to 0.9)
            probability = min(0.9, fraud_score * 0.15)
            prediction = probability > 0.5
            
            # Risk levels
            if probability > 0.7:
                risk_level = "high"
            elif probability > 0.4:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "prediction": bool(prediction),
                "probability": round(float(probability), 4),
                "risk_level": risk_level,
                "model_version": self.model_version,
                "features_used": ["amount", "hour", "pattern_rules"]
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                "prediction": False,
                "probability": 0.1,
                "risk_level": "low",
                "model_version": self.model_version,
                "error": str(e)
            }
    
    def predict_batch(self, transactions: list) -> list:
        return [self.predict(tx) for tx in transactions]