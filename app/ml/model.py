import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class FraudDetectionModel:
    """Simplified fraud detection model for PythonAnyWhere"""
    
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.model_version = "1.0.0"
    
    def load_model(self, model_path: str):
        """Load pre-trained model"""
        try:
            # For demo purposes - in real scenario, use joblib.load(model_path)
            # self.model = joblib.load(model_path)
            
            # Create a simple rule-based model for demo
            self.model = "demo_model"
            self.is_loaded = True
            logger.info(f"✅ Model loaded: {model_path}")
            
        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            # Create fallback model
            self.model = "fallback_model"
            self.is_loaded = True
            logger.info("✅ Using fallback rule-based model")
    
    def predict(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict fraud using rule-based approach"""
        if not self.is_loaded:
            raise ValueError("Model not loaded")
        
        try:
            amount = transaction_data.get('amount', 0)
            timestamp = pd.to_datetime(transaction_data.get('timestamp'))
            hour = timestamp.hour
            
            # Simple rule-based fraud detection
            fraud_rules = [
                amount > 5000,  # Large amount
                hour in [0, 1, 2, 3, 4],  # Late night
                amount <= 0,  # Invalid amount
            ]
            
            fraud_score = sum(fraud_rules)
            probability = min(0.95, fraud_score * 0.3)
            prediction = probability > 0.5
            
            # Determine risk level
            if probability > 0.7:
                risk_level = "high"
            elif probability > 0.3:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "prediction": bool(prediction),
                "probability": round(float(probability), 4),
                "risk_level": risk_level,
                "model_version": self.model_version
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            # Return safe default
            return {
                "prediction": False,
                "probability": 0.1,
                "risk_level": "low",
                "model_version": self.model_version
            }
    
    def predict_batch(self, transactions: list) -> list:
        """Predict fraud for multiple transactions"""
        return [self.predict(tx) for tx in transactions]