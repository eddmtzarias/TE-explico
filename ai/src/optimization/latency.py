"""Latency optimization utilities for sub-500ms inference"""

import torch
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class LatencyOptimizer:
    """Optimization strategies for reducing inference latency"""
    
    @staticmethod
    def optimize_model(model: torch.nn.Module, device: str = "cuda") -> torch.nn.Module:
        """Apply various optimization techniques to reduce latency"""
        
        if device == "cuda" and torch.cuda.is_available():
            logger.info("Applying CUDA optimizations...")
            
            # Enable TF32 for better performance on Ampere GPUs
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Enable cuDNN autotuner
            torch.backends.cudnn.benchmark = True
            
            # Convert to half precision if possible
            try:
                model = model.half()
                logger.info("Converted model to FP16")
            except Exception as e:
                logger.warning(f"Failed to convert to FP16: {e}")
        
        # Set to eval mode for inference
        model.eval()
        
        # Compile model (PyTorch 2.0+)
        try:
            import torch._dynamo
            model = torch.compile(model, mode="reduce-overhead")
            logger.info("Model compiled with torch.compile")
        except Exception as e:
            logger.warning(f"torch.compile not available: {e}")
        
        return model
    
    @staticmethod
    def enable_kv_cache():
        """Enable key-value caching for faster generation"""
        # KV caching is enabled by default in Transformers
        # This method is a placeholder for custom implementations
        pass
    
    @staticmethod
    def quantize_model(model: torch.nn.Module) -> torch.nn.Module:
        """Apply dynamic quantization for faster inference"""
        try:
            quantized_model = torch.quantization.quantize_dynamic(
                model,
                {torch.nn.Linear},
                dtype=torch.qint8
            )
            logger.info("Applied dynamic quantization")
            return quantized_model
        except Exception as e:
            logger.warning(f"Quantization failed: {e}")
            return model


class BatchProcessor:
    """Efficient batch processing for multiple requests"""
    
    def __init__(self, max_batch_size: int = 32):
        self.max_batch_size = max_batch_size
        self.pending_requests = []
        
    async def add_request(self, request):
        """Add request to batch queue"""
        self.pending_requests.append(request)
        
        if len(self.pending_requests) >= self.max_batch_size:
            return await self.process_batch()
        
        return None
    
    async def process_batch(self):
        """Process accumulated batch"""
        if not self.pending_requests:
            return []
        
        batch = self.pending_requests[:self.max_batch_size]
        self.pending_requests = self.pending_requests[self.max_batch_size:]
        
        # Process batch
        # Implementation depends on specific model requirements
        return batch


class CacheManager:
    """Simple LRU cache for frequently requested inferences"""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def get(self, key: str) -> Optional[dict]:
        """Get cached result"""
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, key: str, value: dict):
        """Cache a result"""
        if key in self.cache:
            self.access_order.remove(key)
        
        self.cache[key] = value
        self.access_order.append(key)
        
        # Evict oldest if over capacity
        if len(self.cache) > self.max_size:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
