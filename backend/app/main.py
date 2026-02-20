"""
Main FastAPI Application - Exoplanet Intelligence System
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
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

# Standard CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Belt-and-suspenders: also inject CORS headers via middleware decorator
# This fires on EVERY request, guaranteeing headers are always present.
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Handle OPTIONS preflight directly
    if request.method == "OPTIONS":
        origin = request.headers.get("origin", "*")
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "86400",
            },
        )
    response = await call_next(request)
    origin = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


# ===============================
# Include API Routes
# ===============================

app.include_router(router, prefix="/api")

# ===============================
# Startup Event
# ===============================

@app.on_event("startup")
async def startup_event():
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

# ===============================
# Shutdown Event
# ===============================

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down API...")
    await close_db()

# ===============================
# Root Endpoint
# ===============================

@app.get("/")
async def root():
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

# ===============================
# Health Check
# ===============================

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# ===============================
# Global Exception Handler
# ===============================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )

# ===============================
# Local Run (Development Only)
# ===============================

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