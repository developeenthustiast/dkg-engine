"""
Input Validation using Pydantic
Provides models and validators for all TruthGraph data structures
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, validator, root_validator
from enum import Enum


class BiasLeaning(str, Enum):
    """Enum for bias detection results"""
    LEFT = "left"
    RIGHT = "right"
    NEUTRAL = "neutral"
    CENTER_LEFT = "center_left"
    CENTER_RIGHT = "center_right"


class ArticleSource(BaseModel):
    """Validated article/source data"""
    url: HttpUrl
    text: str = Field(..., min_length=1, max_length=1_000_000)
    citations: List[str] = Field(default_factory=list, max_items=1000)
    timestamp: datetime
    content_hash: str = Field(..., pattern=r'^sha256:[a-f0-9]{64}$')
    
    @validator('text')
    def sanitize_text(cls, v):
        """Remove potential XSS or injection attacks"""
        # Remove null bytes
        v = v.replace('\x00', '')
        return v.strip()


class ComparisonRequest(BaseModel):
    """Request to compare two claims"""
    claim1: str = Field(..., min_length=1, max_length=10000)
    claim2: str = Field(..., min_length=1, max_length=10000)
    context: Optional[str] = Field(None, max_length=50000)
    
    @validator('claim1', 'claim2', 'context')
    def sanitize_input(cls, v):
        if v is None:
            return v
        v = v.replace('\x00', '')
        return v.strip()


class ComparisonResult(BaseModel):
    """Result of claim comparison"""
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    conflict: bool
    explanation: str = Field(..., max_length=5000)
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: List[ArticleSource] = Field(default_factory=list)


class HallucinationRequest(BaseModel):
    """Request to detect hallucinations"""
    text: str = Field(..., min_length=1, max_length=50000)
    context: Optional[str] = Field(None, max_length=50000)
    
    @validator('text', 'context')
    def sanitize_input(cls, v):
        if v is None:
            return v
        v = v.replace('\x00', '')
        return v.strip()


class HallucinationResult(BaseModel):
    """Result of hallucination detection"""
    is_hallucination: bool
    score: float = Field(..., ge=0.0, le=1.0)
    segments: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)


class BiasRequest(BaseModel):
    """Request to analyze bias"""
    text: str = Field(..., min_length=1, max_length=50000)
    
    @validator('text')
    def sanitize_input(cls, v):
        v = v.replace('\x00', '')
        return v.strip()


class BiasResult(BaseModel):
    """Result of bias analysis"""
    bias_score: float = Field(..., ge=0.0, le=1.0)
    leaning: BiasLeaning
    explanation: str = Field(..., max_length=5000)
    confidence: float = Field(..., ge=0.0, le=1.0)


class DKGPublishRequest(BaseModel):
    """Request to publish to DKG"""
    data: Dict[str, Any]
    schema_type: str = Field(..., pattern=r'^[a-z_]+$')
    
    @validator('schema_type')
    def validate_schema_type(cls, v):
        allowed = ['comparison', 'community_note', 'hallucination']
        if v not in allowed:
            raise ValueError(f'schema_type must be one of {allowed}')
        return v


class MCPToolRequest(BaseModel):
    """Generic MCP tool request"""
    tool_name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-z_]+$')
    parameters: Dict[str, Any]
    
    @validator('parameters')
    def validate_params(cls, v):
        # Prevent excessively large payloads
        import json
        if len(json.dumps(v)) > 100_000:
            raise ValueError('Parameters payload too large')
        return v


class WikipediaSearchRequest(BaseModel):
    """Request to search Wikipedia"""
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(10, ge=1, le=50)
    
    @validator('query')
    def sanitize_query(cls, v):
        v = v.replace('\x00', '')
        return v.strip()


class RateLimitConfig(BaseModel):
    """Configuration for rate limiting"""
    requests_per_second: float = Field(..., gt=0, le=1000)
    burst_size: int = Field(10, ge=1, le=100)


def validate_input(model: type[BaseModel]):
    """Decorator to validate function inputs using Pydantic models"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # First arg is usually 'self', skip it
            if args and hasattr(args[0], '__class__'):
                validated = model(**kwargs)
            else:
                # If no self, validate first positional arg
                if args:
                    validated = model(**args[0] if isinstance(args[0], dict) else vars(args[0]))
                else:
                    validated = model(**kwargs)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
