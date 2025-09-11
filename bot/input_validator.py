import click

# Allowed trading symbols on Binance Futures Testnet
ALLOWED_SYMBOLS = {"BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOTUSDT"}

# Allowed order types (including bonus STOP_LIMIT)
ALLOWED_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}

# Allowed order sides
ALLOWED_SIDES = {"BUY", "SELL"}


def symbol_validator(ctx, param, value):
    """Validate trading symbol against allowed pairs."""
    if not value:
        raise click.BadParameter("Symbol is required")

    symbol_upper = value.upper()
    if symbol_upper not in ALLOWED_SYMBOLS:
        raise click.BadParameter(
            f"Symbol must be one of {sorted(ALLOWED_SYMBOLS)}. "
            f"Got: {value}"
        )
    return symbol_upper


def quantity_validator(ctx, param, value):
    """Validate order quantity - must be positive number."""
    if value is None:
        raise click.BadParameter("Quantity is required")

    if value <= 0:
        raise click.BadParameter(
            f"Quantity must be greater than zero. Got: {value}"
        )

    # Check minimum quantity (typical futures minimum is 0.001)
    if value < 0.001:
        raise click.BadParameter(
            f"Quantity too small. Minimum: 0.001. Got: {value}"
        )

    return value


def price_validator(ctx, param, value):
    """Validate price - must be positive when provided."""
    if value is not None and value <= 0:
        raise click.BadParameter(
            f"Price must be greater than zero. Got: {value}"
        )
    return value


def stop_price_validator(ctx, param, value):
    """Validate stop price for STOP_LIMIT orders."""
    if value is not None and value <= 0:
        raise click.BadParameter(
            f"Stop price must be greater than zero. Got: {value}"
        )
    return value


def order_type_validator(ctx, param, value):
    """Validate order type against allowed types."""
    if not value:
        raise click.BadParameter("Order type is required")

    order_type_upper = value.upper()
    if order_type_upper not in ALLOWED_ORDER_TYPES:
        raise click.BadParameter(
            f"Order type must be one of {sorted(ALLOWED_ORDER_TYPES)}. "
            f"Got: {value}"
        )
    return order_type_upper


def side_validator(ctx, param, value):
    """Validate order side (BUY/SELL)."""
    if not value:
        raise click.BadParameter("Order side is required")

    side_upper = value.upper()
    if side_upper not in ALLOWED_SIDES:
        raise click.BadParameter(
            f"Order side must be one of {sorted(ALLOWED_SIDES)}. "
            f"Got: {value}"
        )
    return side_upper


def validate_order_requirements(order_type, price, stop_price):
    """
    Cross-validate order requirements based on order type.
    Called from cli.py after all inputs are collected.
    """
    if order_type == "LIMIT" and price is None:
        raise click.BadParameter("LIMIT orders require --price parameter")

    if order_type == "STOP_LIMIT":
        if price is None:
            raise click.BadParameter("STOP_LIMIT orders require --price parameter")
        if stop_price is None:
            raise click.BadParameter("STOP_LIMIT orders require --stop parameter")
        if stop_price <= 0 or price <= 0:
            raise click.BadParameter("STOP_LIMIT orders require positive price and stop price")

    if order_type == "MARKET" and (price is not None or stop_price is not None):
        click.echo("Warning: MARKET orders ignore price parameters", err=True)


def get_symbol_info():
    """Return information about allowed symbols for help text."""
    return {
        "symbols": sorted(ALLOWED_SYMBOLS),
        "order_types": sorted(ALLOWED_ORDER_TYPES),
        "sides": sorted(ALLOWED_SIDES)
    }
