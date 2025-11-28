"""
Configuration Management for TruthGraph
Loads configuration from environment with validation
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from truthgraph.exceptions import ConfigurationException, MissingConfigException


@dataclass
class APIConfig:
    """API-related configuration"""
    wikipedia_api_url: str = "https://en.wikipedia.org/w/api.php"
    wikipedia_rate_limit: int = 10  # requests per second
    wikipedia_timeout: int = 30  # seconds
    
    # Grok/X AI API
    grok_api_url: str = "https://api.x.ai/v1"
    grok_timeout: int = 60
    
    # DKG configuration
    dkg_endpoint: str = field(default_factory=lambda: os.getenv("DKG_NODE_ENDPOINT", "http://localhost:8900"))
    dkg_timeout: int = 30
    
    def __post_init__(self):
        """Validate API configuration"""
        if self.wikipedia_rate_limit <= 0:
            raise ConfigurationException("wikipedia_rate_limit must be positive")
        if self.wikipedia_rate_limit > 100:
            raise ConfigurationException("wikipedia_rate_limit too high (max 100)")


@dataclass
class SecretsConfig:
    """Secrets and API keys - loaded from environment only"""
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    grok_api_key: Optional[str] = field(default_factory=lambda: os.getenv("GROK_API_KEY"))
    dkg_private_key: Optional[str] = field(default_factory=lambda: os.getenv("DKG_PRIVATE_KEY"))
    dkg_publisher_id: Optional[str] = field(default_factory=lambda: os.getenv("DKG_PUBLISHER_ID"))
    
    def require_openai(self) -> str:
        """Get OpenAI API key or raise exception"""
        if not self.openai_api_key:
            raise MissingConfigException("OPENAI_API_KEY")
        return self.openai_api_key
    
    def require_anthropic(self) -> str:
        """Get Anthropic API key or raise exception"""
        if not self.anthropic_api_key:
            raise MissingConfigException("ANTHROPIC_API_KEY")
        return self.anthropic_api_key
    
    def require_grok(self) -> str:
        """Get Grok API key or raise exception"""
        if not self.grok_api_key:
            raise MissingConfigException("GROK_API_KEY")
        return self.grok_api_key
    
    def require_dkg_credentials(self) -> tuple[str, str]:
        """Get DKG credentials or raise exception"""
        if not self.dkg_private_key:
            raise MissingConfigException("DKG_PRIVATE_KEY")
        if not self.dkg_publisher_id:
            raise MissingConfigException("DKG_PUBLISHER_ID")
        return self.dkg_private_key, self.dkg_publisher_id


@dataclass
class CacheConfig:
    """Caching configuration"""
    enabled: bool = True
    ttl_seconds: int = 3600  # 1 hour default
    max_size_mb: int = 100
    
    def __post_init__(self):
        if self.ttl_seconds < 0:
            raise ConfigurationException("cache_ttl_seconds must be non-negative")
        if self.max_size_mb < 1:
            raise ConfigurationException("cache_max_size_mb must be positive")


@dataclass
class SecurityConfig:
    """Security-related configuration"""
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 60
    require_authentication: bool = field(
        default_factory=lambda: os.getenv("REQUIRE_AUTHENTICATION", "true").lower() == "true"
    )
    allowed_origins: list[str] = field(
        default_factory=lambda: os.getenv("ALLOWED_ORIGINS", "*").split(",")
    )
    max_request_size_mb: int = 10
    
    def __post_init__(self):
        if self.rate_limit_requests_per_minute < 1:
            raise ConfigurationException("rate_limit_requests_per_minute must be positive")


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    json_format: bool = field(
        default_factory=lambda: os.getenv("LOG_JSON", "true").lower() == "true"
    )
    log_dir: Path = field(default_factory=lambda: Path(os.getenv("LOG_DIR", "logs")))
    
    def __post_init__(self):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.level.upper() not in valid_levels:
            raise ConfigurationException(f"log_level must be one of {valid_levels}")


class Config:
    """Main configuration class"""
    
    def __init__(self):
        self.api = APIConfig()
        self.secrets = SecretsConfig()
        self.cache = CacheConfig()
        self.security = SecurityConfig()
        self.logging = LoggingConfig()
        
        # Environment
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = self.environment == "development"
        
        # Legacy compatibility
        self.OPENAI_API_KEY = self.secrets.openai_api_key
        self.ANTHROPIC_API_KEY = self.secrets.anthropic_api_key
        self.GROK_API_KEY = self.secrets.grok_api_key
    
    def validate(self) -> None:
        """Validate all configuration"""
        # All validation is done in __post_init__ methods
        pass
    
    def __repr__(self) -> str:
        """Safe repr that doesn't expose secrets"""
        return (
            f"Config(environment={self.environment}, "
            f"debug={self.debug}, "
            f"api={self.api}, "
            f"cache={self.cache}, "
            f"security={self.security})"
        )


# Global configuration instance
config = Config()


# Convenience function to reload configuration
def reload_config() -> Config:
    """Reload configuration from environment"""
    global config
    config = Config()
    return config