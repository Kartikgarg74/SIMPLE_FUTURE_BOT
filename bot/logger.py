import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
try:
    import binance
    binance_version = binance.__version__
except ImportError:
    binance_version = "Not installed"

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "trading.log"

# Ensure logs directory exists
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str = "trading_bot"):
    """
    Returns a configured logger with both file and console handlers.

    Features:
    - Rotating file handler (1MB max, 5 backups)
    - Console output for real-time monitoring
    - Structured formatting with timestamps
    - UTF-8 encoding for international symbols
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if logger is reused
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create formatter with ISO timestamp
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    # File handler with rotation (required for submission)
    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=1_000_000,  # 1MB per file
        backupCount=5,       # Keep 5 backup files
        encoding="utf-8"     # Support international characters
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler for immediate feedback
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent propagation to root logger (avoid duplicates)
    logger.propagate = False

    return logger


def setup_root_logging():
    """
    Configure root logger for catching any unhandled exceptions.
    Call this once at application startup.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)

    # Only add file handler to root to avoid console spam
    if not root_logger.hasHandlers():
        file_handler = RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=1_000_000,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.WARNING)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | ROOT | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def log_system_info():
    """Log system and environment information for debugging."""
    logger = get_logger("system")
    import platform

    try:
        import binance
        binance_version = binance.__version__
    except ImportError:
        binance_version = "Not installed"

    logger.info("=" * 50)
    logger.info("TRADING BOT STARTUP")
    logger.info("=" * 50)
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"python-binance version: {binance_version}")
    logger.info(f"Log file: {LOG_FILE.absolute()}")
    logger.info("=" * 50)


def get_log_stats():
    """
    Return statistics about the current log file.
    Useful for monitoring and debugging.
    """
    if not LOG_FILE.exists():
        return {"exists": False}

    stat = LOG_FILE.stat()
    return {
        "exists": True,
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / 1_000_000, 2),
        "modified": stat.st_mtime
    }
