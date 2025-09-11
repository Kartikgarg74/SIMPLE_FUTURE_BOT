# Binance Futures Trading Bot

A professional Python trading bot for Binance Futures```stnet (USDT-M) with comprehensive CLI interface, input validation, and logging capabilities.

## 🎯 Project Overview

This trading bot was built to meet the requirements of a Python```veloper hiring assessment. It demonstrates```ofessional software development practices while providing a fully functional trading interface``` Binance Futures Testnet.```## ✅ Requirements Met

- **✅ Python Language**: Built entirely in Python 3.8+
- **✅ Market & Limit Orders**: Full support for both order types
- **✅ BUY/SELL Support**: Complete bidirectional trading capability
- **✅ Official Binance API**: Uses `python-binance` library with REST endpoints
- **✅ CLI Interface**: Professional command-line interface with validation
- **✅ Order Details Output**: Comprehensive order```ecution status display
- **✅ Logging & Error Handling**: Rotating```le logs with full error tracking
- **✅ Bonus: STOP_LIMIT Orders**: Advance```rder type implementation```## 🏗️ Architecture

```
simple_futures_bot/
├── bot/                    # Core trading bot package
│   ├── __init__.py        # Package exports
│   ├── client_manager.py  # Binance API connection management
│   ├── order_executor.py  # Order placement and management
│   ├── input_validator.py # CLI input validation functions
│   └── logger.py          # Logging configuration
├── cli.py                 # Main CLI application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── logs/                 # Auto-created log directory
    └── trading.log       # Rotating log files
```

## 🚀 Quick Start

### Prerequisites

1. **Binance Futures Testnet Account``` Register at [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. **API Credentials**: Generate API key and secret from your test``` account
3. **Python 3.8+**: Ensure Python is installed on your system

### Installation

```
# Clone the repository
git clone <your-repo-url>
cd simple_futures_bot

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API credentials
```

### Configuration

Edit `.env` file with your Binance Futures Testnet credentials:`````
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_secret_here
```

## 📋 Usage Examples

### Interactive Mode
```
python cli.py
```
Follow the interactive prompts to place orders.

### Command Line Arguments
```
# Market order
python cli.py --symbol BTCUSDT --side BUY --qty 0.01 --otype MARKET

# Limit order
python cli.py --symbol ETHUSDT --side SELL --qty 0.1 --otype LIMIT --price 2500

# Stop-limit order (bonus feature)
python cli.py --symbol BTCUSDT --side BUY --qty 0.005 --otype STOP_LIMIT --price 65000 --stop 64000

# Skip confirmation prompt
python cli.py --symbol BTCUSDT --side BUY --qty 0.01 --otype MARKET --no-confirm
```

### Utility Commands
```
# Test connection
python cli.py test

# System information
python cli.py info
```

## 🛠️ Technical Features

### Professional CLI Interface
- **Input validation** with clear error messages
- **Interactive prompts** for missing parameters
- **Order confirmation** with summary```splay
- **Help system** with usage examples

### Robust Error Handling
- **Binance API exceptions** handled gracefully
- **Connection validation** before trading
- **Parameter validation** for all order types
- **User-friendly error messages**

### Comprehensive Logging
- **Rotating file logs** (1MB max, 5 backups)
- **API request/response logging** for audit trail```**Error logging** with full stack traces
- **System information logging** for debugging

### Order Management
- **Real-time order status** display
- **Order confirmation** details
- **Balance checking** capabilities
- **Symbol validation** against supporte```airs

## 📊 Supported Trading Pairs

- **BTCUSDT** - Bitcoin/Tether
- **ETHUSDT** - Ethereum/Tether
- **BNBUSDT** - Binance Coin/Tether
- **ADAUSDT** - Cardano/Tether
- **DOTUSDT** - Polkadot/Tether

## 📝 Log Files

All trading activity is logged to `logs/trading.log` with:
- **Timestamped entries** in ISO 8601 format
- **API requests and responses** in JSON format
- **Error details** with full exception information
- **System startup information** for debugging

Example log entry:
```
2025-09-11T09:30:00 | INFO     | trading_bot | Placing MARKET order: {"symbol": "BTCUSDT", "side": "BUY", "quantity": 0.01, "type": "MARKET"}
2025-09-11T09:30:01 | INFO     | trading_bot | Order executed successfully: {"orderId": 123456789, "symbol": "BTCUSDT", "status": "FILLED"}
```

## 🔒 Security Features

- **Environment variable storage** for API```edentials
- **Testnet-only operation** (no live trading risk)
- **Input validation** prevents malformed requests```**Error logging** without exposing sensitive data```# 🧪 Testing

```
# Test Binance connection
python cli.py test

# Verify installation
python cli.py info

# Place small test orders
python cli.py --symbol BTCUSDT --side BUY --qty 0.001 --otype MARKET
```

## 📦 Dependencies

**Core Requirements:**
- `python-binance==1.0.17` - Official Binance API client
- `python-dotenv==1.0.0` - Environment variable management
- `click==8.1.7` - Professional CLI framework

**Optional Enhancements:**
- `rich==13.7.0` - Enhanced terminal output
- `colorama==0.4.6` - Cross-platform colored text

See `requirements.txt` for complete dependency list.

## 🎓 Educational Value

This project demonstrates:
- **API Integration** with financial services
- **Professional Python packaging** and project structure
- **Command-line application development** with Click
- **Logging and error handling** best practices
- **Input validation and user experience**```sign
- **Environment-based configuration** management

## 📄 License

MIT License - This project is for educational and hiring assessment```rposes.

## 🤝 Assignment Submission

This trading bot fulfills all requirements for the "```ior Python Developer –```ypto Trading Bot" position```1. ✅ **Language**: Python
2. ✅ **Order Types**: MARKET and LIMIT (plus bonus STOP_LIMIT)
3. ✅ **Order Sides**: BUY and SELL support
4. ✅ **API Integration**: Official Binance REST API
5. ✅ **CLI Interface**: Comprehensive command-line interface
6. ✅ **Output Display**: Detailed order execution status``` ✅ **Logging**: Complete request/response/```or logging
8. ✅ **Bonus Feature**: STOP_LIMIT order type implemented

**Ready for submission with logs demonstrating successful order placement on Binance Futures Testnet```
