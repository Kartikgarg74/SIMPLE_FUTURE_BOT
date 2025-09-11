#!/usr/bin/env python3
"""
Binance Futures Trading Bot CLI
===============================

Command-line interface for placing orders on Binance Futures Testnet (USDT-M).
Supports MARKET, LIMIT, and STOP_LIMIT order types with comprehensive validation and logging.

Usage:
    python cli.py --symbol BTCUSDT --side BUY --qty 0.01 --otype MARKET
    python cli.py --symbol ETHUSDT --side SELL --qty 0.1 --otype LIMIT --price 2500.0
    python cli.py --symbol BTCUSDT --side BUY --qty 0.005 --otype STOP_LIMIT --price 65000 --stop 64000

Environment Variables:
    API_KEY: Binance Futures Testnet API Key
    API_SECRET: Binance Futures Testnet API Secret
"""

import os
import sys
import click
from pathlib import Path

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from bot import ClientManager, place_order
from bot.input_validator import (
    symbol_validator,
    quantity_validator,
    price_validator,
    stop_price_validator,
    order_type_validator,
    side_validator,
    validate_order_requirements,
    get_symbol_info
)
from bot.logger import get_logger, setup_root_logging, log_system_info
from dotenv import load_dotenv
load_dotenv()  # Force load .env file

# Initialize logging
setup_root_logging()
logger = get_logger("cli")

def display_banner():
    """Display application banner and information."""
    click.echo("=" * 60)
    click.echo("🚀 BINANCE FUTURES TRADING BOT")
    click.echo("   Testnet Environment (USDT-M Futures)")
    click.echo("=" * 60)

    # Show available symbols and order types
    info = get_symbol_info()
    click.echo(f"📈 Supported symbols: {', '.join(info['symbols'])}")
    click.echo(f"📋 Order types: {', '.join(info['order_types'])}")
    click.echo(f"🔄 Order sides: {', '.join(info['sides'])}")
    click.echo("-" * 60)


def validate_environment():
    """Validate that required environment variables are set."""
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        click.echo("❌ Error: Missing API credentials", err=True)
        click.echo("Please set the following environment variables:", err=True)
        click.echo("  - API_KEY: Your Binance Futures Testnet API Key", err=True)
        click.echo("  - API_SECRET: Your Binance Futures Testnet API Secret", err=True)
        click.echo("", err=True)
        click.echo("Example:", err=True)
        click.echo("  export API_KEY=your_api_key_here", err=True)
        click.echo("  export API_SECRET=your_api_secret_here", err=True)
        sys.exit(1)

    return api_key, api_secret


def prompt_for_missing_params(otype: str, price: float, stop_price: float):
    """Prompt user for missing required parameters based on order type."""

    if otype == "LIMIT" and price is None:
        price = click.prompt("Enter limit price", type=float)
        price = price_validator(None, None, price)

    elif otype == "STOP_LIMIT":
        if price is None:
            price = click.prompt("Enter limit price", type=float)
            price = price_validator(None, None, price)

        if stop_price is None:
            stop_price = click.prompt("Enter stop price", type=float)
            stop_price = stop_price_validator(None, None, stop_price)

    return price, stop_price


@click.command()
@click.option(
    "--symbol",
    callback=symbol_validator,
    prompt="Trading symbol",
    help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
)
@click.option(
    "--side",
    callback=side_validator,
    prompt="Order side",
    help="Order side: BUY or SELL"
)
@click.option(
    "--qty",
    type=float,
    callback=quantity_validator,
    prompt="Quantity",
    help="Order quantity (minimum: 0.001)"
)
@click.option(
    "--otype",
    callback=order_type_validator,
    prompt="Order type",
    help="Order type: MARKET, LIMIT, or STOP_LIMIT"
)
@click.option(
    "--price",
    type=float,
    callback=price_validator,
    default=None,
    help="Limit price (required for LIMIT and STOP_LIMIT orders)"
)
@click.option(
    "--stop",
    "stop_price",
    type=float,
    callback=stop_price_validator,
    default=None,
    help="Stop price (required for STOP_LIMIT orders)"
)
@click.option(
    "--confirm/--no-confirm",
    default=True,
    help="Prompt for confirmation before placing order"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose logging output"
)
def main(symbol, side, qty, otype, price, stop_price, confirm, verbose):
    """
    Binance Futures Trading Bot CLI

    Place MARKET, LIMIT, or STOP_LIMIT orders on Binance Futures Testnet (USDT-M).
    All orders are placed using the testnet environment for safe testing.

    Examples:
        python cli.py --symbol BTCUSDT --side BUY --qty 0.01 --otype MARKET
        python cli.py --symbol ETHUSDT --side SELL --qty 0.1 --otype LIMIT --price 2500
    """

    # Show banner
    display_banner()

    # Log startup info
    log_system_info()
    logger.info("CLI started with parameters: symbol=%s, side=%s, qty=%s, otype=%s",
                symbol, side, qty, otype)

    try:
        # Validate environment
        api_key, api_secret = validate_environment()

        # Prompt for missing parameters based on order type
        price, stop_price = prompt_for_missing_params(otype, price, stop_price)

        # Final validation of order requirements
        validate_order_requirements(otype, price, stop_price)

        # Display order summary
        click.echo("\n📋 ORDER SUMMARY")
        click.echo("-" * 30)
        click.echo(f"Symbol:       {symbol}")
        click.echo(f"Side:         {side}")
        click.echo(f"Quantity:     {qty}")
        click.echo(f"Order Type:   {otype}")

        if price is not None:
            click.echo(f"Price:        {price}")
        if stop_price is not None:
            click.echo(f"Stop Price:   {stop_price}")

        click.echo("-" * 30)

        # Confirmation prompt
        if confirm:
            if not click.confirm("\n🔍 Do you want to place this order?"):
                click.echo("❌ Order cancelled by user")
                logger.info("Order cancelled by user")
                sys.exit(0)

        # Initialize client and place order
        click.echo("\n🔗 Connecting to Binance Futures Testnet...")
        client_manager = ClientManager(api_key, api_secret, testnet=True)

        click.echo("📡 Placing order...")
        response = place_order(
            client_manager.client,
            symbol=symbol,
            side=side,
            quantity=qty,
            order_type=otype,
            price=price,
            stop_price=stop_price
        )

        logger.info("Order completed successfully: %s", response.get('orderId'))
        click.echo("\n✅ Trading bot execution completed successfully!")

    except click.BadParameter as e:
        error_msg = f"❌ Invalid parameter: {e}"
        click.echo(error_msg, err=True)
        logger.error("Parameter validation error: %s", e)
        sys.exit(1)

    except Exception as e:
        error_msg = f"❌ Trading bot error: {e}"
        click.echo(error_msg, err=True)
        logger.error("Unexpected error: %s", e, exc_info=True)
        sys.exit(1)


@click.group()
def cli():
    """Binance Futures Trading Bot Command Line Interface"""
    pass


@cli.command()
def info():
    """Display bot information and supported symbols."""
    display_banner()

    click.echo("\n📊 SYSTEM INFORMATION")
    click.echo("-" * 30)

    import platform
    try:
        import binance
        binance_version = binance.__version__
    except:
        binance_version = "Unknown"

    click.echo(f"Python:           {platform.python_version()}")
    click.echo(f"Platform:         {platform.system()} {platform.release()}")
    click.echo(f"python-binance:   {binance_version}")
    click.echo(f"Log file:         logs/trading.log")

    # Check environment
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    click.echo(f"API Key:          {'✅ Set' if api_key else '❌ Not set'}")
    click.echo(f"API Secret:       {'✅ Set' if api_secret else '❌ Not set'}")


@cli.command()
def test():
    """Test connection to Binance Futures Testnet."""
    click.echo("🧪 Testing connection to Binance Futures Testnet...")

    try:
        api_key, api_secret = validate_environment()
        client_manager = ClientManager(api_key, api_secret, testnet=True)

        # Test connection by getting account info
        balance = client_manager.get_account_balance()
        click.echo("✅ Connection test successful!")
        click.echo(f"📊 Account has {len(balance)} asset balances")

        # Show USDT balance if available
        for asset in balance:
            if asset['asset'] == 'USDT':
                click.echo(f"💰 USDT Balance: {asset['balance']}")
                break

    except Exception as e:
        click.echo(f"❌ Connection test failed: {e}", err=True)
        sys.exit(1)


# Add the main command to the CLI group
cli.add_command(main, name="order")

if __name__ == "__main__":
    # If called directly, run the main order placement command
    cli()
