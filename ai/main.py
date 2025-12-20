from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import uvicorn
import os
from typing import Optional
import logging

from src.inference.engine import InferenceEngine
from src.utils.metrics import setup_metrics, track_inference_time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global inference engine
inference_engine: Optional[InferenceEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application"""
    global inference_engine
    
    # Startup
    logger.info("Initializing inference engine...")
    inference_engine = InferenceEngine()
    await inference_engine.initialize()
    logger.info("Inference engine ready")
    
    yield
    
    # Shutdown
    logger.info("Shutting down inference engine...")
    if inference_engine:
        await inference_engine.shutdown()


app = FastAPI(
    title="TE-explico AI Service",
    description="OmniMaestro AI Inference Engine with <500ms latency target",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:4000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup metrics
setup_metrics(app)


class InferenceRequest(BaseModel):
    context: str = Field(..., max_length=10000, description="User's context or screenshot text")
    question: str = Field(..., max_length=1000, description="User's question")


class InferenceResponse(BaseModel):
    answer: str
    confidence: float
    latency_ms: float
    model_version: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": inference_engine is not None and inference_engine.is_ready,
    }


@app.post("/infer", response_model=InferenceResponse)
@track_inference_time
async def infer(request: InferenceRequest):
    """Main inference endpoint"""
    if not inference_engine or not inference_engine.is_ready:
        raise HTTPException(status_code=503, detail="Model not ready")
    
    try:
        result = await inference_engine.infer(
            context=request.context,
            question=request.question,
        )
        return result
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=1,
        log_level="info",
    )
