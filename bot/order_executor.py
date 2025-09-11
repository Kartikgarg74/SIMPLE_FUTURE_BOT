from binance.exceptions import BinanceAPIException, BinanceOrderException
from .logger import get_logger
import json

logger = get_logger()

def place_order(client, symbol: str, side: str, quantity: float, order_type: str,
                price: float = None, stop_price: float = None):
    """
    Place an order on Binance Futures (USDT-M Testnet).
    Supports MARKET, LIMIT, and STOP_LIMIT order types.
    """

    # Validate order parameters
    _validate_order_params(order_type, price, stop_price)

    # Build order parameters
    params = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "type": order_type,
    }

    # Add timeInForce for non-market orders
    if order_type in ["LIMIT", "STOP_LIMIT"]:
        params["timeInForce"] = "GTC"

    # Add price parameters based on order type
    if order_type == "LIMIT":
        params["price"] = str(price)
    elif order_type == "STOP_LIMIT":
        params["price"] = str(price)
        params["stopPrice"] = str(stop_price)

    try:
        # Log the request
        logger.info(f"Placing {order_type} order: {json.dumps(params, default=str)}")

        # Execute the order
        response = client.futures_create_order(**params)

        # Log successful response
        logger.info(f"Order executed successfully: {json.dumps(response, default=str)}")

        # Display order details to user
        _display_order_success(response, order_type)

        return response

    except BinanceAPIException as e:
        error_msg = f"Binance API error: {e}"
        logger.error(error_msg)
        print(f"❌ Order failed: {error_msg}")
        raise
    except BinanceOrderException as e:
        error_msg = f"Order error: {e}"
        logger.error(error_msg)
        print(f"❌ Order rejected: {error_msg}")
        raise
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logger.error(error_msg)
        print(f"❌ Order failed: {error_msg}")
        raise

def _validate_order_params(order_type: str, price: float, stop_price: float):
    """Validate order parameters based on order type."""
    if order_type == "LIMIT" and price is None:
        raise ValueError("LIMIT orders require a price parameter")

    if order_type == "STOP_LIMIT":
        if price is None or stop_price is None:
            raise ValueError("STOP_LIMIT orders require both price and stop_price parameters")
        if price <= 0 or stop_price <= 0:
            raise ValueError("Price and stop_price must be positive values")

def _display_order_success(response: dict, order_type: str):
    """Display formatted order success message to user."""
    order_id = response.get("orderId", "N/A")
    symbol = response.get("symbol", "N/A")
    side = response.get("side", "N/A")
    quantity = response.get("origQty", "N/A")
    status = response.get("status", "N/A")

    print("\n✅ ORDER EXECUTED SUCCESSFULLY")
    print("=" * 40)
    print(f"Order ID: {order_id}")
    print(f"Symbol: {symbol}")
    print(f"Side: {side}")
    print(f"Type: {order_type}")
    print(f"Quantity: {quantity}")
    print(f"Status: {status}")

    # Show price info for limit orders
    if "price" in response and response["price"] != "0":
        print(f"Price: {response['price']}")

    # Show stop price for stop-limit orders
    if "stopPrice" in response and response["stopPrice"] != "0":
        print(f"Stop Price: {response['stopPrice']}")

    print("=" * 40)
    print()

def get_order_status(client, symbol: str, order_id: int):
    """
    Check the status of a specific order.

    Parameters:
    - client: authenticated python-binance Client instance
    - symbol: trading pair symbol
    - order_id: order ID to check

    Returns:
    - dict: Order status information
    """
    try:
        logger.info(f"Checking order status for ID: {order_id}")
        response = client.futures_get_order(symbol=symbol, orderId=order_id)
        logger.info(f"Order status retrieved: {json.dumps(response, default=str)}")
        return response

    except BinanceAPIException as e:
        error_msg = f"Failed to get order status: {e}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        raise


def cancel_order(client, symbol: str, order_id: int):
    """
    Cancel an open order.

    Parameters:
    - client: authenticated python-binance Client instance
    - symbol: trading pair symbol
    - order_id: order ID to cancel

    Returns:
    - dict: Cancellation response
    """
    try:
        logger.info(f"Cancelling order ID: {order_id}")
        response = client.futures_cancel_order(symbol=symbol, orderId=order_id)
        logger.info(f"Order cancelled: {json.dumps(response, default=str)}")
        print(f"✅ Order {order_id} cancelled successfully")
        return response

    except BinanceAPIException as e:
        error_msg = f"Failed to cancel order: {e}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        raise


def get_open_orders(client, symbol: str = None):
    """
    Get all open orders for a symbol or all symbols.

    Parameters:
    - client: authenticated python-binance Client instance
    - symbol: trading pair symbol (optional, if None gets all open orders)

    Returns:
    - list: List of open orders
    """
    try:
        params = {"symbol": symbol} if symbol else {}
        logger.info(f"Fetching open orders: {params}")

        response = client.futures_get_open_orders(**params)
        logger.info(f"Retrieved {len(response)} open orders")

        if response:
            print(f"\n📋 Open Orders ({len(response)} found):")
            print("-" * 60)
            for order in response:
                print(f"ID: {order['orderId']} | {order['symbol']} | "
                      f"{order['side']} {order['origQty']} @ {order.get('price', 'MARKET')}")
        else:
            print("📋 No open orders found")

        return response

    except BinanceAPIException as e:
        error_msg = f"Failed to get open orders: {e}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        raise
