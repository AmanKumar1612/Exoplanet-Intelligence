"""
Main FastAPI Application - Exoplanet Intelligence System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes import router
from database import init_db, close_db
from model_loader import load_models

# Create FastAPI app
app = FastAPI(
    title="Exoplanet Intelligence System API",
    description="ML-powered predictions for exoplanet classification and radius estimation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
# Define CORS origins explicitly
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex="https?://(localhost|127\.0\.0\.1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Authorization"],
)

# Include routers
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("=" * 60)
    print("Starting Exoplanet Intelligence System API")
    print("=" * 60)
    
    # Initialize database
    try:
        await init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"⚠ Database initialization warning: {e}")
    
    # Load ML models
    try:
        load_models()
        print("✓ ML models loaded")
    except Exception as e:
        print(f"⚠ Model loading warning: {e}")
    
    print("=" * 60)
    print("API Ready")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down API...")
    await close_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Exoplanet Intelligence System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
        "endpoints": {
            "classification": "/api/predict/classification",
            "regression": "/api/predict/regression",
            "history": "/api/predictions/history",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )
