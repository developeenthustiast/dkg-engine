"""
Custom Exception Hierarchy for TruthGraph
Provides structured error handling with error codes
"""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(str, Enum):
    """Standard error codes for TruthGraph"""
    # Validation errors (1000-1999)
    VALIDATION_ERROR = "E1000"
    INVALID_INPUT = "E1001"
    MISSING_REQUIRED_FIELD = "E1002"
    INVALID_FORMAT = "E1003"
    
    # Authentication/Authorization (2000-2999)
    AUTHENTICATION_FAILED = "E2000"
    UNAUTHORIZED = "E2001"
    FORBIDDEN = "E2003"
    INVALID_TOKEN = "E2004"
    TOKEN_EXPIRED = "E2005"
    
    # Rate Limiting (3000-3999)
    RATE_LIMIT_EXCEEDED = "E3000"
    QUOTA_EXCEEDED = "E3001"
    
    # External API errors (4000-4999)
    EXTERNAL_API_ERROR = "E4000"
    WIKIPEDIA_API_ERROR = "E4001"
    DKG_API_ERROR = "E4002"
    API_TIMEOUT = "E4003"
    API_UNAVAILABLE = "E4004"
    
    # Data processing errors (5000-5999)
    PROCESSING_ERROR = "E5000"
    COMPARISON_FAILED = "E5001"
    HALLUCINATION_DETECTION_FAILED = "E5002"
    BIAS_ANALYSIS_FAILED = "E5003"
    
    # Storage errors (6000-6999)
    STORAGE_ERROR = "E6000"
    DKG_PUBLISH_ERROR = "E6001"
    CACHE_ERROR = "E6002"
    
    # Configuration errors (7000-7999)
    CONFIGURATION_ERROR = "E7000"
    MISSING_CONFIG = "E7001"
    INVALID_CONFIG = "E7002"
    
    # System errors (9000-9999)
    INTERNAL_ERROR = "E9000"
    NOT_IMPLEMENTED = "E9001"
    SERVICE_UNAVAILABLE = "E9002"


class TruthGraphException(Exception):
    """Base exception for all TruthGraph errors"""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        result = {
            'error': {
                'code': self.error_code.value,
                'message': self.message,
                'details': self.details
            }
        }
        
        if self.cause:
            result['error']['cause'] = str(self.cause)
        
        return result
    
    def __str__(self) -> str:
        return f"[{self.error_code.value}] {self.message}"


# Validation Exceptions

class ValidationException(TruthGraphException):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        details = kwargs.pop('details', {})
        if field:
            details['field'] = field
        super().__init__(
            message,
            error_code=ErrorCode.VALIDATION_ERROR,
            details=details,
            **kwargs
        )


class InvalidInputException(ValidationException):
    """Raised for invalid input data"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code=ErrorCode.INVALID_INPUT, **kwargs)


class MissingRequiredFieldException(ValidationException):
    """Raised when required field is missing"""
    def __init__(self, field: str, **kwargs):
        super().__init__(
            f"Required field '{field}' is missing",
            field=field,
            error_code=ErrorCode.MISSING_REQUIRED_FIELD,
            **kwargs
        )


# Authentication/Authorization Exceptions

class AuthenticationException(TruthGraphException):
    """Base exception for authentication errors"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.AUTHENTICATION_FAILED,
            **kwargs
        )


class UnauthorizedException(AuthenticationException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication required", **kwargs):
        super().__init__(message, error_code=ErrorCode.UNAUTHORIZED, **kwargs)


class ForbiddenException(AuthenticationException):
    """Raised when user lacks permissions"""
    def __init__(self, message: str = "Access forbidden", **kwargs):
        super().__init__(message, error_code=ErrorCode.FORBIDDEN, **kwargs)


class InvalidTokenException(AuthenticationException):
    """Raised for invalid authentication tokens"""
    def __init__(self, message: str = "Invalid authentication token", **kwargs):
        super().__init__(message, error_code=ErrorCode.INVALID_TOKEN, **kwargs)


# Rate Limiting Exceptions

class RateLimitException(TruthGraphException):
    """Raised when rate limit is exceeded"""
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        details = kwargs.pop('details', {})
        if retry_after:
            details['retry_after'] = retry_after
        super().__init__(
            message,
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            details=details,
            **kwargs
        )


# External API Exceptions

class ExternalAPIException(TruthGraphException):
    """Base exception for external API errors"""
    def __init__(self, message: str, service: str, **kwargs):
        details = kwargs.pop('details', {})
        details['service'] = service
        super().__init__(
            message,
            error_code=ErrorCode.EXTERNAL_API_ERROR,
            details=details,
            **kwargs
        )


class WikipediaAPIException(ExternalAPIException):
    """Raised when Wikipedia API fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            service="Wikipedia",
            error_code=ErrorCode.WIKIPEDIA_API_ERROR,
            **kwargs
        )


class DKGAPIException(ExternalAPIException):
    """Raised when DKG API fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            service="DKG",
            error_code=ErrorCode.DKG_API_ERROR,
            **kwargs
        )


class APITimeoutException(ExternalAPIException):
    """Raised when API call times out"""
    def __init__(self, service: str, timeout: float, **kwargs):
        super().__init__(
            f"{service} API timeout after {timeout}s",
            service=service,
            error_code=ErrorCode.API_TIMEOUT,
            **kwargs
        )


# Processing Exceptions

class ProcessingException(TruthGraphException):
    """Base exception for data processing errors"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.PROCESSING_ERROR,
            **kwargs
        )


class ComparisonFailedException(ProcessingException):
    """Raised when claim comparison fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.COMPARISON_FAILED,
            **kwargs
        )


class HallucinationDetectionFailedException(ProcessingException):
    """Raised when hallucination detection fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.HALLUCINATION_DETECTION_FAILED,
            **kwargs
        )


# Storage Exceptions

class StorageException(TruthGraphException):
    """Base exception for storage errors"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.STORAGE_ERROR,
            **kwargs
        )


class DKGPublishException(StorageException):
    """Raised when DKG publish fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.DKG_PUBLISH_ERROR,
            **kwargs
        )


# Configuration Exceptions

class ConfigurationException(TruthGraphException):
    """Raised for configuration errors"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.CONFIGURATION_ERROR,
            **kwargs
        )


class MissingConfigException(ConfigurationException):
    """Raised when required configuration is missing"""
    def __init__(self, config_key: str, **kwargs):
        super().__init__(
            f"Missing required configuration: {config_key}",
            error_code=ErrorCode.MISSING_CONFIG,
            details={'config_key': config_key},
            **kwargs
        )


# System Exceptions

class NotImplementedException(TruthGraphException):
    """Raised for not-yet-implemented features"""
    def __init__(self, feature: str, **kwargs):
        super().__init__(
            f"Feature not yet implemented: {feature}",
            error_code=ErrorCode.NOT_IMPLEMENTED,
            details={'feature': feature},
            **kwargs
        )


class ServiceUnavailableException(TruthGraphException):
    """Raised when service is temporarily unavailable"""
    def __init__(self, message: str = "Service temporarily unavailable", **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
            **kwargs
        )
