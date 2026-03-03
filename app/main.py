from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import db_manager
from .api import warehouse, shipping


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler for startup and shutdown events.
    """
    # Startup
    await db_manager.connect()
    yield
    # Shutdown
    await db_manager.disconnect()


# Create FastAPI application
app = FastAPI(
    title="E-Commerce Shipping Charge Estimator",
    description="B2B e-commerce marketplace shipping charge calculator for Kirana stores",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(warehouse.router)
app.include_router(shipping.router)


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "E-Commerce Shipping Charge Estimator API",
        "status": "active",
        "version": "1.0.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check endpoint"""
    try:
        # Check database connection
        db = db_manager.database
        await db.command("ping")
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"  # In production, use actual time
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )