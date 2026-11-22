import ccxt
import loguru
from loguru import logger
import sys

logger.add(
    "development/plan/memetrading_bot_plan/kucoin_test.log",
    rotation="10 MB",
    backtrace=True,
    diagnose=True
)

def test_kucoin():
    logger.info("Starting KuCoin API test")
    try:
        # Initialize KuCoin exchange
        exchange = ccxt.kucoin({
            'enableRateLimit': True,
        })
        
        # Check if market data is available
        markets = exchange.load_markets()
        btc_market = markets.get('BTC/USDT')
        
        logger.info(f"KuCoin markets loaded: {len(markets)} markets")
        if btc_market:
            logger.info(f"BTC/USDT market found: {btc_market['symbol']}")
        else:
            logger.info("BTC/USDT market not found")
            
        # Fetch ticker
        ticker = exchange.fetch_ticker('BTC/USDT')
        logger.info(f"BTC/USDT price: ${ticker['last']:,.2f}")
        logger.info(f"24h change: {ticker.get('percentageChange', 'N/A')}%")
        
        logger.info("KuCoin test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"KuCoin test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_kucoin()
    logger.info(f"Test {'passed' if success else 'failed'}")
    sys.exit(0 if success else 1)