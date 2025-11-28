"""
Circuit Breaker Pattern Implementation
Prevents cascading failures in external API calls
"""

import time
from enum import Enum
from typing import Callable, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """States for circuit breaker"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failure threshold exceeded
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout: float = 60.0  # seconds


class CircuitBreakerOpenException(Exception):
    """Raised when circuit breaker is open"""
    pass


class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures
    
    States:
    - CLOSED: Normal operation, calls pass through
    - OPEN: Too many failures, calls blocked
    - HALF_OPEN: Testing recovery, limited calls allowed
    """
    
    def __init__(self, config: CircuitBreakerConfig = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.last_attempt_time = 0.0
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Function result
        
        Raises:
            CircuitBreakerOpenException: When circuit is open
        """
        if not self._can_attempt():
            raise CircuitBreakerOpenException(
                f"Circuit breaker is {self.state.value}, blocking call"
            )
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _can_attempt(self) -> bool:
        """Check if call attempts are allowed"""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if timeout has elapsed
            if time.time() - self.last_failure_time >= self.config.timeout:
                logger.info("Circuit breaker transitioning to HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                return True
            return False
        
        # HALF_OPEN state - allow attempts
        return True
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                logger.info("Circuit breaker transitioning to CLOSED")
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def _on_failure(self):
        """Handle failed call"""
        self.last_failure_time = time.time()
        self.failure_count += 1
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker transitioning to OPEN (failure in HALF_OPEN)")
            self.state = CircuitState.OPEN
            self.success_count = 0
        elif self.failure_count >= self.config.failure_threshold:
            logger.warning(f"Circuit breaker transitioning to OPEN ({self.failure_count} failures)")
            self.state = CircuitState.OPEN
    
    def reset(self):
        """Manually reset circuit breaker"""
        logger.info("Circuit breaker manually reset to CLOSED")
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
