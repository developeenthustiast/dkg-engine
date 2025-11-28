"""
Structured Logging Configuration for TruthGraph
Provides JSON logging with correlation IDs and log rotation
"""

import logging
import logging.handlers
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from contextvars import ContextVar

# Context variable for correlation ID across async calls
correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default='')


class CorrelationIDFilter(logging.Filter):
    """Adds correlation ID to log records"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get() or 'N/A'
        return True


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'correlation_id': getattr(record, 'correlation_id', 'N/A'),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        # Add any extra fields
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        return json.dumps(log_data)


def setup_logging(
    log_level: str = "INFO",
    log_dir: Path = Path("logs"),
    enable_console: bool = True,
    enable_file: bool = True,
    json_format: bool = True
) -> None:
    """
    Configure logging for TruthGraph
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        enable_console: Whether to log to console
        enable_file: Whether to log to file
        json_format: Whether to use JSON formatting
    """
    # Create logs directory if it doesn't exist
    if enable_file:
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(correlation_id)s] - %(message)s'
        )
    
    # Add correlation ID filter
    correlation_filter = CorrelationIDFilter()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        console_handler.addFilter(correlation_filter)
        root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if enable_file:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir / "truthgraph.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        file_handler.addFilter(correlation_filter)
        root_logger.addHandler(file_handler)
        
        # Separate error log
        error_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir / "truthgraph-errors.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        error_handler.addFilter(correlation_filter)
        root_logger.addHandler(error_handler)
    
    # Log configuration complete
    logging.info(f"Logging configured - Level: {log_level}, JSON: {json_format}")


def set_correlation_id(correlation_id: str = None) -> str:
    """
    Set correlation ID for request tracking
    
    Args:
        correlation_id: Correlation ID (generated if not provided)
    
    Returns:
        The correlation ID that was set
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    
    correlation_id_var.set(correlation_id)
    return correlation_id


def get_correlation_id() -> str:
    """Get current correlation ID"""
    return correlation_id_var.get() or 'N/A'


def log_with_extra(logger: logging.Logger, level: int, message: str, **extra) -> None:
    """
    Log a message with extra structured data
    
    Args:
        logger: Logger instance
        level: Log level
        message: Log message
        **extra: Additional structured data
    """
    extra_record = logger.makeRecord(
        logger.name, level, '', 0, message, (), None
    )
    extra_record.extra_data = extra
    logger.handle(extra_record)


# Configure logging on module import
setup_logging()
