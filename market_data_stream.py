#!/usr/bin/env python3
"""
Market Data Stream for real-time price updates using ccxt.
Listens to Binance and MEXC markets for ticker updates.
"""
import ccxt
import time
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarketDataStream:
    """Streams market data from Binance and MEXC exchanges."""
    
    def __init__(self):
        """Initialize exchange connections."""
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
            logger.info("Binance market data stream initialized")
            
            # Initialize MEXC
            self.exchanges['mexc'] = ccxt.mexc({
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'},
            })
            logger.info("MEXC market data stream initialized")
            
        except Exception as e:
            logger.error(f"Error initializing market data streams: {e}")
            raise
    
    def fetch_ticker_continuously(self, exchange: str, symbol: str, 
                                interval: float = 5.0):
        """
        Continuously fetch ticker data at regular intervals.
        
        Args:
            exchange: Exchange name ('binance' or 'mexc')
            symbol: Trading symbol (e.g., 'BTC/USDT')
            interval: Update interval in seconds
        """
        try:
            if exchange not in self.exchanges:
                logger.error(f"Exchange {exchange} not initialized")
                return
            
            logger.info(f"Starting market data stream for {symbol} on {exchange}")
            
            while True:
                try:
                    ticker = self.exchanges[exchange].fetch_ticker(symbol)
                    logger.info(f"{exchange} {symbol} - Last: {ticker['last']}, Volume: {ticker['quoteVolume']}")
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Error fetching ticker: {e}")
                    time.sleep(interval)
                    
        except KeyboardInterrupt:
            logger.info("Market data stream stopped by user")
        except Exception as e:
            logger.error(f"Error in market data stream: {e}")
            raise

if __name__ == "__main__":
    stream = MarketDataStream()
    
    # Example usage - fetch BTC/USDT from Binance every 5 seconds
    try:
        stream.fetch_ticker_continuously('binance', 'BTC/USDT', 5.0)
    except Exception as e:
        logger.error(f"Failed to run market data stream: {e}")