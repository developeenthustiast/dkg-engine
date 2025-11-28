"""
Simple In-Memory Cache with TTL
For caching API responses and computation results
"""

import time
import hashlib
import json
from typing import Any, Optional, Callable
from dataclasses import dataclass
from functools import wraps
import logging

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Cache entry with expiration"""
    value: Any
    expiry_time: float


class SimpleCache:
    """
    Simple in-memory cache with TTL
    Thread-safe for basic operations
    """
    
    def __init__(self, default_ttl: int = 3600, max_size: int = 1000):
        """
        Initialize cache
        
        Args:
            default_ttl: Default time-to-live in seconds
            max_size: Maximum number of entries
        """
        self._cache: dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        entry = self._cache.get(key)
        
        if entry is None:
            self.misses += 1
            return None
        
        # Check if expired
        if time.time() > entry.expiry_time:
            del self._cache[key]
            self.misses += 1
            return None
        
        self.hits += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (default: self.default_ttl)
        """
        # Evict oldest entry if cache is full
        if len(self._cache) >= self.max_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.debug(f"Cache full, evicted oldest entry: {oldest_key}")
        
        ttl = ttl or self.default_ttl
        expiry_time = time.time() + ttl
        
        self._cache[key] = CacheEntry(value=value, expiry_time=expiry_time)
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def cleanup_expired(self):
        """Remove all expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time > entry.expiry_time
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            'size': len(self._cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate
        }


def cache_key_from_args(*args, **kwargs) -> str:
    """
    Generate cache key from function arguments
    
    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        MD5 hash of arguments as cache key
    """
    # Create a stable string representation
    key_data = {
        'args': args,
        'kwargs': kwargs
    }
    
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(ttl: Optional[int] = None, cache_instance: Optional[SimpleCache] = None):
    """
    Decorator to cache function results
    
    Args:
        ttl: Time-to-live in seconds
        cache_instance: Cache instance to use (creates new one if None)
    
    Example:
        @cached(ttl=3600)
        async def expensive_operation(arg1, arg2):
            return result
    """
    if cache_instance is None:
        cache_instance = SimpleCache()
    
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{cache_key_from_args(*args, **kwargs)}"
            
            # Check cache
            cached_result = cache_instance.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Call function
            logger.debug(f"Cache miss for {func.__name__}")
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache_instance.set(cache_key, result, ttl)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{cache_key_from_args(*args, **kwargs)}"
            
            # Check cache
            cached_result = cache_instance.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Call function
            logger.debug(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_instance.set(cache_key, result, ttl)
            
            return result
        
        # Return appropriate wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Global cache instance
global_cache = SimpleCache()
