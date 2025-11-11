"""Configuration and utilities for MCP server."""

import logging
from typing import Optional


def setup_logging(level: int = logging.INFO) -> None:
    """
    Set up logging for the MCP server.
    
    Args:
        level: The logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: The logger name
        
    Returns:
        A configured logger instance
    """
    return logging.getLogger(name)
