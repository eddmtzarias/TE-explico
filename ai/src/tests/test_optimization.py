import pytest
from src.optimization.latency import LatencyOptimizer, CacheManager


def test_cache_manager():
    """Test cache functionality"""
    cache = CacheManager(max_size=2)
    
    # Test set and get
    cache.set("key1", {"result": "value1"})
    assert cache.get("key1") == {"result": "value1"}
    
    # Test cache miss
    assert cache.get("nonexistent") is None
    
    # Test eviction
    cache.set("key2", {"result": "value2"})
    cache.set("key3", {"result": "value3"})
    
    # key1 should be evicted
    assert cache.get("key1") is None
    assert cache.get("key2") == {"result": "value2"}
    assert cache.get("key3") == {"result": "value3"}


def test_cache_lru_ordering():
    """Test LRU ordering in cache"""
    cache = CacheManager(max_size=2)
    
    cache.set("key1", {"result": "value1"})
    cache.set("key2", {"result": "value2"})
    
    # Access key1 to make it most recently used
    cache.get("key1")
    
    # Add key3, should evict key2 (least recently used)
    cache.set("key3", {"result": "value3"})
    
    assert cache.get("key1") == {"result": "value1"}
    assert cache.get("key2") is None
    assert cache.get("key3") == {"result": "value3"}
