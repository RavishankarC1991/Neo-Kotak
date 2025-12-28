from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import EXPLICIT_WAIT, TIMEFRAME, CHART_ANALYSIS_DURATION
from logger import get_logger

logger = get_logger(__name__)

class ChartAnalyzer:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logger
    
    def open_chart(self, symbol):
        """Open the candlestick chart for a given stock symbol."""
        try:
            self.logger.info(f"Opening chart for {symbol}")
            
            # Click on the stock row to open chart (adjust selector based on actual structure)
            stock_element = self.driver.find_element(By.XPATH, f"//td[contains(text(), '{symbol}')]")
            stock_element.click()
            
            time.sleep(2)
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'chart-container'))
            )
            
            self.logger.info(f"Chart opened for {symbol}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open chart for {symbol}: {str(e)}")
            raise
    
    def set_timeframe(self, timeframe=TIMEFRAME):
        """Set the chart timeframe to hourly (1H)."""
        try:
            self.logger.info(f"Setting timeframe to {timeframe}")
            
            # Find timeframe button (adjust selector based on actual UI)
            timeframe_buttons = self.driver.find_elements(By.CLASS_NAME, 'timeframe-btn')
            for btn in timeframe_buttons:
                if '1H' in btn.text or '1h' in btn.text.lower():
                    btn.click()
                    time.sleep(1)
                    self.logger.info(f"Timeframe set to {timeframe}")
                    return True
            
            self.logger.warning("Could not find hourly timeframe button, may be already set")
            return False
        except Exception as e:
            self.logger.error(f"Failed to set timeframe: {str(e)}")
            raise
    
    def analyze_current_movement(self):
        """Analyze current stock movement from the chart."""
        try:
            self.logger.info("Analyzing chart movement")
            
            analysis = {
                'current_price': None,
                'price_change': None,
                'price_change_percent': None,
                'high': None,
                'low': None,
                'open': None,
                'close': None,
                'volume': None,
                'trend': None,
                'resistance_levels': [],
                'support_levels': []
            }
            
            # Wait for chart to fully load
            time.sleep(2)
            
            # Extract current price (adjust selector based on actual HTML)
            try:
                current_price_elem = self.driver.find_element(By.CLASS_NAME, 'current-price')
                analysis['current_price'] = current_price_elem.text
                self.logger.info(f"Current Price: {analysis['current_price']}")
            except:
                self.logger.warning("Could not extract current price")
            
            # Extract price change
            try:
                price_change_elem = self.driver.find_element(By.CLASS_NAME, 'price-change')
                analysis['price_change'] = price_change_elem.text
                self.logger.info(f"Price Change: {analysis['price_change']}")
            except:
                self.logger.warning("Could not extract price change")
            
            # Extract OHLC (Open, High, Low, Close) values
            try:
                ohlc_values = self.driver.find_elements(By.CLASS_NAME, 'ohlc-value')
                if len(ohlc_values) >= 4:
                    analysis['open'] = ohlc_values[0].text
                    analysis['high'] = ohlc_values[1].text
                    analysis['low'] = ohlc_values[2].text
                    analysis['close'] = ohlc_values[3].text
                    self.logger.info(f"OHLC - O:{analysis['open']} H:{analysis['high']} L:{analysis['low']} C:{analysis['close']}")
            except:
                self.logger.warning("Could not extract OHLC values")
            
            # Determine trend (simple: if close > open, uptrend; else downtrend)
            try:
                candle_color = self.driver.find_element(By.CLASS_NAME, 'candle').get_attribute('class')
                if 'bullish' in candle_color or 'green' in candle_color:
                    analysis['trend'] = 'UPTREND'
                elif 'bearish' in candle_color or 'red' in candle_color:
                    analysis['trend'] = 'DOWNTREND'
                else:
                    analysis['trend'] = 'NEUTRAL'
                self.logger.info(f"Trend: {analysis['trend']}")
            except:
                self.logger.warning("Could not determine trend")
            
            # Analyze for 5 minutes (default) before moving on
            self.logger.info(f"Analyzing chart for {CHART_ANALYSIS_DURATION} seconds")
            time.sleep(CHART_ANALYSIS_DURATION)
            
            return analysis
        except Exception as e:
            self.logger.error(f"Failed to analyze chart: {str(e)}")
            raise
    
    def take_screenshot(self, filename):
        """Take a screenshot of the current chart."""
        try:
            self.logger.info(f"Taking screenshot: {filename}")
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return False
    
    def close_chart(self):
        """Close the chart and return to portfolio."""
        try:
            self.logger.info("Closing chart")
            close_btn = self.driver.find_element(By.CLASS_NAME, 'close-chart')
            close_btn.click()
            time.sleep(1)
            self.logger.info("Chart closed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to close chart: {str(e)}")
            return False
