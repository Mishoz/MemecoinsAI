#!/usr/bin/env python3
"""
Order Executor for basic buy/sell operations using ccxt.
Executes market orders on Binance and MEXC exchanges.
"""
import ccxt
import logging
import asyncio
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OrderExecutor:
    """Executes basic market orders on exchanges."""
    
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
            logger.info("Binance order executor initialized")
            
            # Initialize MEXC
            self.exchanges['mexc'] = ccxt.mexc({
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'},
            })
            logger.info("MEXC order executor initialized")
            
        except Exception as e:
            logger.error(f"Error initializing order executor: {e}")
            raise
    
    def execute_market_order(self, exchange: str, symbol: str, 
                           side: str, amount: float) -> Optional[Dict]:
        """
        Execute a market order on specified exchange.
        
        Args:
            exchange: Exchange name ('binance' or 'mexc')
            symbol: Trading symbol (e.g., 'BTC/USDT')
            side: 'buy' or 'sell'
            amount: Amount to trade
        
        Returns:
            Order response or None if error
        """
        try:
            if exchange not in self.exchanges:
                logger.error(f"Exchange {exchange} not initialized")
                return None
            
            order_side = 'buy' if side.lower() == 'buy' else 'sell'
            
            logger.info(f"Executing {order_side} order on {exchange}: {amount} {symbol}")
            
            order = self.exchanges[exchange].create_market_order(
                symbol,
                order_side,
                amount
            )
            
            logger.info(f"Order executed successfully: {order['id']} on {exchange}")
            return order
            
        except Exception as e:
            logger.error(f"Error executing market order on {exchange}: {e}")
            return None
    
    def close(self):
        """Close all exchange connections."""
        for exchange_name, exchange in self.exchanges.items():
            try:
                exchange.close()
                logger.info(f"Closed connection to {exchange_name}")
            except Exception as e:
                logger.error(f"Error closing {exchange_name}: {e}")

if __name__ == "__main__":
    executor = OrderExecutor()
    
    try:
        # Example: Execute a buy order for 0.001 BTC on Binance
        # Note: This will actually trade if run with real funds!
        # order = executor.execute_market_order('binance', 'BTC/USDT', 'buy', 0.001)
        # print(f"Order result: {order}")
        
        print("Order executor ready. Call execute_market_order() with proper parameters.")
        
    except Exception as e:
        logger.error(f"Error in order executor: {e}")
    finally:
        executor.close()