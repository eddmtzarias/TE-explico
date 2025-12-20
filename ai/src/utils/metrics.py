from prometheus_client import Counter, Histogram, Gauge
from fastapi import FastAPI
import time
import functools
import logging

logger = logging.getLogger(__name__)

# Define metrics
inference_requests = Counter(
    'inference_requests_total',
    'Total number of inference requests',
    ['status']
)

inference_latency = Histogram(
    'inference_latency_seconds',
    'Inference latency in seconds',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0, 2.0, 5.0]
)

model_loaded = Gauge(
    'model_loaded',
    'Whether the model is loaded and ready'
)

active_requests = Gauge(
    'active_inference_requests',
    'Number of currently active inference requests'
)


def setup_metrics(app: FastAPI):
    """Setup metrics collection for the application"""
    logger.info("Metrics collection initialized")
    

def track_inference_time(func):
    """Decorator to track inference time and metrics"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        active_requests.inc()
        
        try:
            result = await func(*args, **kwargs)
            inference_requests.labels(status='success').inc()
            return result
        except Exception as e:
            inference_requests.labels(status='error').inc()
            raise
        finally:
            latency = time.perf_counter() - start_time
            inference_latency.observe(latency)
            active_requests.dec()
            
            # Log if latency exceeds target
            if latency > 0.5:  # 500ms
                logger.warning(f"Inference latency exceeded target: {latency*1000:.2f}ms")
    
    return wrapper
