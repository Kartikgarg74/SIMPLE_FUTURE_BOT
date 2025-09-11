"""
simple_futures_bot.bot package

This package contains all the core trading bot functionality:
- ClientManager: Binance API connection management
- order_executor: Order placement and management functions
- input_validator: CLI input validation functions
- logger: Logging configuration and utilities

Usage:
    from bot import ClientManager, place_order
    from bot.input_validator import symbol_validator
"""

from .client_manager import ClientManager
from .order_executor import (
    place_order,
    get_order_status,
    cancel_order,
    get_open_orders
)
from .input_validator import (
    symbol_validator,
    quantity_validator,
    price_validator,
    stop_price_validator,
    order_type_validator,
    side_validator,
    validate_order_requirements,
    get_symbol_info
)
from .logger import (
    get_logger,
    setup_root_logging,
    log_system_info,
    get_log_stats
)

__version__ = "1.0.0"

__all__ = [
    # Core classes
    "ClientManager",

    # Order execution functions
    "place_order",
    "get_order_status",
    "cancel_order",
    "get_open_orders",

    # Input validators
    "symbol_validator",
    "quantity_validator",
    "price_validator",
    "stop_price_validator",
    "order_type_validator",
    "side_validator",
    "validate_order_requirements",
    "get_symbol_info",

    # Logging utilities
    "get_logger",
    "setup_root_logging",
    "log_system_info",
    "get_log_stats"
]
