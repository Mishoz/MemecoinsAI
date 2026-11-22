import requests
import loguru
from loguru import logger
import sys

# Configure logging
logger.add(
    "development/plan/memetrading_bot_plan/coinGecko_api_test.log",
    rotation="10 MB",
    backtrace=True,
    diagnose=True
)

def fetch_coingecko_data(coin_id: str = 'bitcoin'):
    """Fetch data from CoinGecko API using requests"""
    try:
        # CoinGecko API endpoint for coin data
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        logger.info(f"Fetching data from {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully fetched data for {coin_id}")
        
        # Extract relevant information
        price = data.get('market_data', {}).get('current_price', {}).get('usd')
        market_cap = data.get('market_data', {}).get('market_cap', {}).get('usd')
        
        logger.info(f"Price: ${price:,.2f} if price else N/A")
        logger.info(f"Market Cap: ${market_cap:,.2f} if market_cap else N/A")
        
        return {
            'price': price,
            'market_cap': market_cap,
            'data': data
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def main():
    logger.info("Starting CoinGecko API test")
    result = fetch_coingecko_data('bitcoin')
    
    if result and result.get('price'):
        logger.info("CoinGecko API test passed")
        sys.exit(0)
    else:
        logger.error("CoinGecko API test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()