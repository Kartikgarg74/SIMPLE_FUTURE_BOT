"""
Tests for bot/input_validator.py

Covers valid and invalid inputs for all validator functions,
plus cross-field validation via validate_order_requirements.
"""

import pytest
import click

import sys
from pathlib import Path

# Ensure the project root is importable regardless of cwd
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.input_validator import (
    symbol_validator,
    quantity_validator,
    price_validator,
    stop_price_validator,
    order_type_validator,
    side_validator,
    validate_order_requirements,
    get_symbol_info,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _call(fn, value):
    """Call a Click-style validator with dummy ctx/param."""
    return fn(None, None, value)


# ---------------------------------------------------------------------------
# Test 1: symbol_validator — valid symbol (case-insensitive)
# ---------------------------------------------------------------------------

def test_symbol_validator_valid():
    assert _call(symbol_validator, "btcusdt") == "BTCUSDT"
    assert _call(symbol_validator, "ETHUSDT") == "ETHUSDT"


# ---------------------------------------------------------------------------
# Test 2: symbol_validator — invalid symbol raises BadParameter
# ---------------------------------------------------------------------------

def test_symbol_validator_invalid():
    with pytest.raises(click.BadParameter):
        _call(symbol_validator, "XYZUSDT")


# ---------------------------------------------------------------------------
# Test 3: symbol_validator — empty string raises BadParameter
# ---------------------------------------------------------------------------

def test_symbol_validator_empty():
    with pytest.raises(click.BadParameter):
        _call(symbol_validator, "")


# ---------------------------------------------------------------------------
# Test 4: quantity_validator — valid quantity passes through unchanged
# ---------------------------------------------------------------------------

def test_quantity_validator_valid():
    assert _call(quantity_validator, 0.001) == 0.001
    assert _call(quantity_validator, 1.5) == 1.5


# ---------------------------------------------------------------------------
# Test 5: quantity_validator — zero and negative values raise BadParameter
# ---------------------------------------------------------------------------

def test_quantity_validator_invalid_zero_and_negative():
    with pytest.raises(click.BadParameter):
        _call(quantity_validator, 0)
    with pytest.raises(click.BadParameter):
        _call(quantity_validator, -1.0)


# ---------------------------------------------------------------------------
# Test 6: quantity_validator — below minimum (0.001) raises BadParameter
# ---------------------------------------------------------------------------

def test_quantity_validator_below_minimum():
    with pytest.raises(click.BadParameter):
        _call(quantity_validator, 0.0009)


# ---------------------------------------------------------------------------
# Test 7: price_validator and stop_price_validator — None passes through
# ---------------------------------------------------------------------------

def test_price_validator_none_allowed():
    assert _call(price_validator, None) is None
    assert _call(stop_price_validator, None) is None


# ---------------------------------------------------------------------------
# Test 8: price_validator — non-positive value raises BadParameter
# ---------------------------------------------------------------------------

def test_price_validator_non_positive():
    with pytest.raises(click.BadParameter):
        _call(price_validator, 0.0)
    with pytest.raises(click.BadParameter):
        _call(price_validator, -100.0)


# ---------------------------------------------------------------------------
# Test 9: order_type_validator — valid types normalised to upper-case
# ---------------------------------------------------------------------------

def test_order_type_validator_valid():
    assert _call(order_type_validator, "market") == "MARKET"
    assert _call(order_type_validator, "LIMIT") == "LIMIT"
    assert _call(order_type_validator, "stop_limit") == "STOP_LIMIT"


# ---------------------------------------------------------------------------
# Test 10: order_type_validator — unknown type raises BadParameter
# ---------------------------------------------------------------------------

def test_order_type_validator_invalid():
    with pytest.raises(click.BadParameter):
        _call(order_type_validator, "FOO")


# ---------------------------------------------------------------------------
# Test 11: side_validator — BUY/SELL normalised; invalid raises BadParameter
# ---------------------------------------------------------------------------

def test_side_validator_valid_and_invalid():
    assert _call(side_validator, "buy") == "BUY"
    assert _call(side_validator, "SELL") == "SELL"
    with pytest.raises(click.BadParameter):
        _call(side_validator, "LONG")


# ---------------------------------------------------------------------------
# Test 12: validate_order_requirements — LIMIT without price raises
# ---------------------------------------------------------------------------

def test_validate_order_requirements_limit_missing_price():
    with pytest.raises(click.BadParameter):
        validate_order_requirements("LIMIT", None, None)


# ---------------------------------------------------------------------------
# Test 13: validate_order_requirements — STOP_LIMIT requires both price and stop
# ---------------------------------------------------------------------------

def test_validate_order_requirements_stop_limit_missing_stop():
    with pytest.raises(click.BadParameter):
        validate_order_requirements("STOP_LIMIT", 65000.0, None)

    with pytest.raises(click.BadParameter):
        validate_order_requirements("STOP_LIMIT", None, 64000.0)


# ---------------------------------------------------------------------------
# Test 14: validate_order_requirements — valid STOP_LIMIT does not raise
# ---------------------------------------------------------------------------

def test_validate_order_requirements_stop_limit_valid():
    # Should not raise
    validate_order_requirements("STOP_LIMIT", 65000.0, 64000.0)


# ---------------------------------------------------------------------------
# Test 15: get_symbol_info — returns expected keys and non-empty sets
# ---------------------------------------------------------------------------

def test_get_symbol_info_structure():
    info = get_symbol_info()
    assert "symbols" in info
    assert "order_types" in info
    assert "sides" in info
    assert len(info["symbols"]) > 0
    assert "BTCUSDT" in info["symbols"]
    assert "MARKET" in info["order_types"]
    assert "BUY" in info["sides"]
