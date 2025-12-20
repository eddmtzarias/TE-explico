import pytest
import asyncio
from src.inference.engine import InferenceEngine


@pytest.mark.asyncio
async def test_inference_engine_initialization():
    """Test that inference engine initializes correctly"""
    engine = InferenceEngine()
    await engine.initialize()
    
    assert engine.is_ready
    assert engine.model is not None
    assert engine.tokenizer is not None
    
    await engine.shutdown()


@pytest.mark.asyncio
async def test_inference_latency():
    """Test that inference meets latency requirements"""
    engine = InferenceEngine()
    await engine.initialize()
    
    result = await engine.infer(
        context="Testing the application",
        question="What should I test?"
    )
    
    assert result['latency_ms'] < 500  # p95 target
    assert 'answer' in result
    assert result['confidence'] > 0
    
    await engine.shutdown()


@pytest.mark.asyncio
async def test_prompt_construction():
    """Test prompt construction"""
    engine = InferenceEngine()
    
    prompt = engine._construct_prompt("Test context", "Test question")
    
    assert "OmniMaestro" in prompt
    assert "Test context" in prompt
    assert "Test question" in prompt


def test_device_selection():
    """Test device selection logic"""
    engine = InferenceEngine()
    
    assert engine.device in ["cuda", "cpu"]
