import ccxt
import loguru
from loguru import logger
import sys

logger.add(
    "development/plan/memetrading_bot_plan/binance_test.log",
    rotation="10 MB",
    backtrace=True,
    diagnose=True
)

def test_binance():
    logger.info("Starting Binance API test")
    try:
        # Initialize Binance exchange
        exchange = ccxt.binance({
            'enableRateLimit': True,
        })
        
        # Fetch Bitcoin ticker
        logger.info("Fetching Bitcoin ticker from Binance")
        btc = exchange.fetch_ticker('BTC/USDT')
        
        price = btc.get('last')
        bid = btc.get('bid')
        ask = btc.get('ask')
        
        logger.info(f"Bitcoin price on Binance: ${price:,.2f} if price else N/A")
        logger.info(f"Bid: ${bid:,.2f} if bid else N/A")
        logger.info(f"Ask: ${ask:,.2f} if ask else N/A")
        
        # Check for percentage change if available
        if 'percentageChange' in btc:
            logger.info(f"24h change: {btc['percentageChange']}%")
        else:
            logger.info("24h change not available")
            
        logger.info("Binance test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Binance test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_binance()
    logger.info(f"Test {'passed' if success else 'failed'}")
    sys.exit(0 if success else 1)