#!/usr/bin/env python3
"""
Exchange Connector for Binance and MEXC using ccxt library.
Provides unified interface for market data and trading operations.
"""
import ccxt
import logging
from typing import Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExchangeConnector:
    """Unified connector for Binance and MEXC exchanges."""
    
    def __init__(self):
        """Initialize exchange connectors."""
        self.exchanges = {}
        self._initialize_exchanges()
    
    def _initialize_exchanges(self):
        """Initialize Binance and MEXC connectors."""
        try:
            # Initialize Binance
            self.exchanges['binance'] = ccxt.binance({
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'},
            })
            logger.info("Binance connector initialized")
            
            # Initialize MEXC
            self.exchanges['mexc'] = ccxt.mexc({
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'},
            })
            logger.info("MEXC connector initialized")
            
        except Exception as e:
            logger.error(f"Error initializing exchanges: {e}")
            raise
    
    def get_ticker(self, exchange: str, symbol: str) -> Optional[Dict]:
        """
        Fetch ticker data for a symbol from specified exchange.
        
        Args:
            exchange: Exchange name ('binance' or 'mexc')
            symbol: Trading symbol (e.g., 'BTC/USDT')
        
        Returns:
            Ticker data dictionary or None if error
        """
        try:
            if exchange not in self.exchanges:
                logger.error(f"Exchange {exchange} not initialized")
                return None
            
            ticker = self.exchanges[exchange].fetch_ticker(symbol)
            logger.info(f"Fetched {symbol} from {exchange}")
            return ticker
            
        except Exception as e:
            logger.error(f"Error fetching ticker from {exchange} {symbol}: {e}")
            return None
    
    def close(self):
        """Close all exchange connections."""
        for exchange_name, exchange in self.exchanges.items():
            try:
                exchange.close()
                logger.info(f"Closed connection to {exchange_name}")
            except Exception as e:
                logger.error(f"Error closing {exchange_name}: {e}")