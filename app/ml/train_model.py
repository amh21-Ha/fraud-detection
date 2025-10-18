import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sample_data(n_samples=1000):
    """Generate sample fraud detection data"""
    logger.info(f"Generating {n_samples} sample transactions...")
    
    np.random.seed(42)
    data = []
    
    for i in range(n_samples):
        is_fraud = np.random.choice([0, 1], p=[0.97, 0.03])
        
        if is_fraud:
            amount = np.random.lognormal(7, 1.5)  # Higher amounts for fraud
            hour = np.random.choice([0, 1, 2, 3, 4, 22, 23])  # Unusual hours
        else:
            amount = np.random.lognormal(5, 1)  # Normal amounts
            hour = np.random.randint(6, 22)  # Normal hours
        
        data.append({
            'amount': min(amount, 10000),
            'hour': hour,
            'day_of_week': np.random.randint(0, 7),
            'is_weekend': np.random.choice([0, 1], p=[0.7, 0.3]),
            'is_fraud': is_fraud
        })
    
    return pd.DataFrame(data)

def train_and_save_model():
    """Train and save a simple fraud detection model"""
    logger.info("Training fraud detection model...")
    
    # Generate sample data
    df = generate_sample_data(5000)
    
    # Prepare features and target
    features = ['amount', 'hour', 'day_of_week', 'is_weekend']
    X = df[features]
    y = df['is_fraud']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    logger.info(f"Training accuracy: {train_score:.4f}")
    logger.info(f"Testing accuracy: {test_score:.4f}")
    
    # Save model
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / "fraud_model.pkl"
    joblib.dump(model, model_path)
    
    logger.info(f"✅ Model saved to: {model_path}")
    return model_path

if __name__ == "__main__":
    train_and_save_model()