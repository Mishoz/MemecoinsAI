import ccxt
import loguru
from loguru import logger
import sys
import os

# Configure logging
logger.add(
    "development/plan/memetrading_bot_plan/coinGecko_test.log",
    rotation="10 MB",
    backtrace=True,
    diagnose=True
)

def test_coingecko():
    logger.info("Starting CoinGecko API test")
    try:
        # Initialize CoinGecko exchange
        exchange = ccxt.coingecko({
            'enableRateLimit': True,
        })
        
        # Fetch Bitcoin data
        logger.info("Fetching Bitcoin data from CoinGecko")
        btc = exchange.fetch_ticker('bitcoin', 'usd')
        
        logger.info(f"Bitcoin price: ${btc['last']:,.2f}")
        logger.info(f"24h change: {btc['percentageChange']}%")
        
        # Fetch multiple coins
        logger.info("Fetching multiple coins")
        coins = ['bitcoin', 'ethereum', 'solana']
        for coin in coins:
            try:
                data = exchange.fetch_ticker(coin, 'usd')
                logger.info(f"{coin.capitalize()}: ${data['last']:,.2f}")
            except Exception as e:
                logger.error(f"Error fetching {coin}: {e}")
                
        logger.info("CoinGecko test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"CoinGecko test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_coingecko()
    logger.info(f"Test {'passed' if success else 'failed'}")
    sys.exit(0 if success else 1)