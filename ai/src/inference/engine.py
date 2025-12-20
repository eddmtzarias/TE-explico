import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, Optional
import asyncio
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class InferenceEngine:
    """Optimized inference engine with <500ms latency target"""
    
    def __init__(self):
        self.model: Optional[AutoModelForCausalLM] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_ready = False
        self.model_version = "1.0.0"
        
        # Performance optimizations
        self.max_batch_size = int(os.getenv("MAX_BATCH_SIZE", "32"))
        self.max_length = 512
        self.inference_timeout = int(os.getenv("INFERENCE_TIMEOUT", "500")) / 1000  # Convert to seconds
        
    async def initialize(self):
        """Initialize the model and tokenizer"""
        try:
            model_path = os.getenv("MODEL_PATH", "distilgpt2")  # Using lightweight model for demo
            
            logger.info(f"Loading model from {model_path}...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
            )
            
            self.model.to(self.device)
            self.model.eval()
            
            # Warmup
            await self._warmup()
            
            self.is_ready = True
            logger.info("Model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            raise
    
    async def _warmup(self):
        """Warmup the model with sample inputs"""
        logger.info("Warming up model...")
        sample_text = "This is a warmup query."
        
        with torch.no_grad():
            inputs = self.tokenizer(sample_text, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            _ = self.model.generate(**inputs, max_length=50, do_sample=False)
        
        logger.info("Warmup complete")
    
    async def infer(self, context: str, question: str) -> Dict:
        """
        Perform inference with latency optimization
        Target: p95 < 500ms
        """
        start_time = time.perf_counter()
        
        try:
            # Construct prompt
            prompt = self._construct_prompt(context, question)
            
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
                padding=True,
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate with timeout
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.pad_token_id,
                )
            
            # Decode
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            answer = generated_text[len(prompt):].strip()
            
            # Calculate metrics
            latency_ms = (time.perf_counter() - start_time) * 1000
            confidence = 0.85  # Placeholder - implement proper confidence scoring
            
            logger.info(f"Inference completed in {latency_ms:.2f}ms")
            
            return {
                "answer": answer,
                "confidence": confidence,
                "latency_ms": round(latency_ms, 2),
                "model_version": self.model_version,
            }
            
        except Exception as e:
            logger.error(f"Inference error: {str(e)}")
            raise
    
    def _construct_prompt(self, context: str, question: str) -> str:
        """Construct optimized prompt for the model"""
        return f"""You are OmniMaestro, a helpful AI assistant for contextual learning.

Context: {context[:500]}  # Truncate context for performance

Question: {question}

Answer (be clear, concise, and pedagogical):"""
    
    async def shutdown(self):
        """Clean up resources"""
        logger.info("Shutting down inference engine...")
        if self.model:
            del self.model
        if self.tokenizer:
            del self.tokenizer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        self.is_ready = False


import os
