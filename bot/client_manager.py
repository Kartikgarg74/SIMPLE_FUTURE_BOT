import os
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv
import logging

class ClientManager:
    """
    Manages Binance Futures Client connection with proper error handling,
    validation, and testnet configuration for USDT-M Futures.
    """

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        load_dotenv()

        if not api_key or not api_secret:
            raise ValueError("API key and secret are required")

        self.testnet = testnet
        self.logger = logging.getLogger(__name__)

        try:
            # Create client with testnet=True
            self.client = Client(api_key, api_secret, testnet=testnet)

            if testnet:
                # Set the correct futures testnet URL
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
                self.logger.info("Initialized Binance Futures Testnet client")
            else:
                self.logger.info("Initialized Binance Futures Live client")

            # Validate connection
            self._validate_connection()

        except BinanceAPIException as e:
            self.logger.error(f"Binance API error during initialization: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance client: {e}")
            raise

    def _validate_connection(self):
        """Validate API credentials by fetching account information."""
        try:
            account_info = self.client.futures_account()
            self.logger.info("API connection validated successfully")
            return account_info
        except BinanceAPIException as e:
            self.logger.error(f"API validation failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Connection validation error: {e}")
            raise

    def get_account_balance(self):
        """Get futures account balance information."""
        try:
            return self.client.futures_account_balance()
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get account balance: {e}")
            raise

    def get_current_price(self, symbol: str):
        """Get current price for a symbol."""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get price for {symbol}: {e}")
            raise
