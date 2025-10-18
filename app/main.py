from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path

from app.database import engine, create_tables
from app.models import Base
from app.ml.model import FraudDetectionModel
from app.api.endpoints import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance
fraud_model = None

def create_app():
    """Application factory for PythonAnyWhere"""
    global fraud_model
    
    app = FastAPI(
        title="Financial Fraud Detection API",
        description="Real-time ML fraud detection system",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    # Mount static files
    static_path = Path(__file__).parent.parent / "static"
    app.mount("/static", StaticFiles(directory=static_path), name="static")

    # Load ML model at startup
    @app.on_event("startup")
    async def startup_event():
        global fraud_model
        try:
            create_tables()
            logger.info("✅ Database tables created")
            
            # Lightweight model - no file loading needed
            fraud_model = FraudDetectionModel()
            logger.info("✅ Rule-based fraud detection ready")
            
        except Exception as e:
            logger.error(f"❌ Startup error: {e}")
            fraud_model = FraudDetectionModel()  # Fallback

    # Root endpoint - serve dashboard
    @app.get("/", response_class=HTMLResponse)
    async def read_root():
        try:
            dashboard_path = Path(__file__).parent.parent / "static" / "dashboard.html"
            with open(dashboard_path, "r") as f:
                return HTMLResponse(content=f.read())
        except FileNotFoundError:
            return HTMLResponse(
                content="""
                <html>
                    <body>
                        <h1>Financial Fraud Detection API</h1>
                        <p>API is running successfully!</p>
                        <p><a href="/docs">View API Documentation</a></p>
                        <p><a href="/api/v1/health">Check Health</a></p>
                    </body>
                </html>
                """
            )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy" if fraud_model and fraud_model.is_loaded else "degraded",
            "model_loaded": fraud_model.is_loaded if fraud_model else False,
            "service": "fraud-detection-api",
            "timestamp": datetime.now().isoformat()  # Use regular datetime
        }

    # Dependency function
    async def get_fraud_model():
        if fraud_model is None or not fraud_model.is_loaded:
            raise HTTPException(status_code=503, detail="ML model not available")
        return fraud_model

    # Make dependency available to endpoints
    app.dependency_overrides[get_fraud_model] = get_fraud_model

    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)