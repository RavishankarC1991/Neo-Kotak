from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import EXPLICIT_WAIT, KOTAK_PORTFOLIO_URL
from logger import get_logger

logger = get_logger(__name__)

class PortfolioAnalyzer:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logger
        self.positions = []
    
    def navigate_to_portfolio(self):
        """Navigate to portfolio holdings page."""
        try:
            self.logger.info("Navigating to portfolio page")
            self.driver.get(KOTAK_PORTFOLIO_URL)
            time.sleep(2)
            
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'holdings'))
            )
            
            self.logger.info("Successfully navigated to portfolio")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to portfolio: {str(e)}")
            raise
    
    def get_stock_positions(self):
        """Extract all stock positions from portfolio."""
        try:
            self.logger.info("Fetching stock positions")
            
            # Wait for holdings table to load
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'holding-row'))
            )
            
            # Find all stock rows
            stock_rows = self.driver.find_elements(By.CLASS_NAME, 'holding-row')
            self.logger.info(f"Found {len(stock_rows)} positions")
            
            positions = []
            for row in stock_rows:
                try:
                    # Extract stock details (adjust selectors based on actual HTML structure)
                    symbol = row.find_element(By.CLASS_NAME, 'symbol').text
                    quantity = row.find_element(By.CLASS_NAME, 'quantity').text
                    current_price = row.find_element(By.CLASS_NAME, 'current-price').text
                    pnl = row.find_element(By.CLASS_NAME, 'pnl').text
                    
                    position = {
                        'symbol': symbol,
                        'quantity': quantity,
                        'current_price': current_price,
                        'pnl': pnl
                    }
                    positions.append(position)
                    self.logger.info(f"Stock: {symbol}, Qty: {quantity}, Price: {current_price}, P&L: {pnl}")
                except Exception as e:
                    self.logger.warning(f"Could not extract data from row: {str(e)}")
                    continue
            
            self.positions = positions
            return positions
        except Exception as e:
            self.logger.error(f"Failed to fetch stock positions: {str(e)}")
            raise
    
    def get_position_by_symbol(self, symbol):
        """Get a specific position by stock symbol."""
        for position in self.positions:
            if position['symbol'].upper() == symbol.upper():
                return position
        return None
