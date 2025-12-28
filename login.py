from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
from config import KOTAK_LOGIN_URL, KOTAK_PHONE_NUMBER, KOTAK_PASSWORD, BROWSER, IMPLICIT_WAIT, EXPLICIT_WAIT, HEADLESS
from logger import get_logger

logger = get_logger(__name__)

class KotakLogin:
    def __init__(self):
        self.driver = None
        self.logger = logger
    
    def setup_driver(self):
        """Initialize Selenium WebDriver."""
        try:
            if BROWSER.lower() == 'chrome':
                import shutil
                import os
                options = webdriver.ChromeOptions()
                if HEADLESS:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')

                # Prefer a system-installed chromedriver (Homebrew) when available
                system_paths = [
                    '/opt/homebrew/bin/chromedriver',
                    '/usr/local/bin/chromedriver'
                ]
                chromedriver_path = None

                for p in system_paths:
                    if os.path.exists(p) and os.access(p, os.X_OK):
                        chromedriver_path = p
                        break

                # Fallback to chromedriver on PATH
                if not chromedriver_path:
                    chromedriver_path = shutil.which('chromedriver')

                if chromedriver_path:
                    self.logger.info(f"Using system chromedriver at {chromedriver_path}")
                    try:
                        self.driver = webdriver.Chrome(
                            service=Service(chromedriver_path),
                            options=options
                        )
                    except Exception as e:
                        self.logger.warning(f"System chromedriver failed to start: {e}. Falling back to webdriver-manager.")
                        driver_path = ChromeDriverManager().install()
                        self.driver = webdriver.Chrome(
                            service=Service(driver_path),
                            options=options
                        )
                else:
                    # Fallback to webdriver-manager
                    self.logger.info("No system chromedriver found; using webdriver-manager to download one")
                    driver_path = ChromeDriverManager().install()
                    self.driver = webdriver.Chrome(
                        service=Service(driver_path),
                        options=options
                    )
            elif BROWSER.lower() == 'safari':
                # Use Safari's built-in safaridriver. Ensure Remote Automation is enabled in Safari.
                options = webdriver.SafariOptions()
                if HEADLESS:
                    self.logger.warning("Safari does not support headless mode via safaridriver; continuing without headless.")
                try:
                    self.driver = webdriver.Safari()
                    self.logger.info("WebDriver initialized with Safari")
                except Exception as e:
                    self.logger.error("Failed to initialize Safari WebDriver. Ensure 'Allow Remote Automation' is enabled in Safari > Develop, and run 'safaridriver --enable' if necessary.")
                    raise
            elif BROWSER.lower() == 'firefox':
                options = webdriver.FirefoxOptions()
                if HEADLESS:
                    options.add_argument('--headless')
                self.driver = webdriver.Firefox(
                    service=Service(GeckoDriverManager().install()),
                    options=options
                )
            else:
                raise ValueError(f"Unsupported browser: {BROWSER}")
            
            self.driver.implicitly_wait(IMPLICIT_WAIT)
            self.logger.info(f"WebDriver initialized with {BROWSER}")
            return self.driver
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise
    
    def login(self):
        """Log into Kotak Securities."""
        try:
            self.logger.info(f"Navigating to {KOTAK_LOGIN_URL}")
            self.driver.get(KOTAK_LOGIN_URL)
            time.sleep(2)
            
            # Wait for login page to load
            try:
                WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                    EC.presence_of_element_located((By.NAME, 'uid'))
                )
            except Exception as e:
                self.logger.error(f"Form field 'uid' not found within {EXPLICIT_WAIT}s: {e}")
                self.logger.info("Current page URL: " + self.driver.current_url)
                self.logger.info("Page title: " + self.driver.title)
                
                # Take screenshot for debugging
                screenshot_path = "login_page_debug.png"
                self.driver.save_screenshot(screenshot_path)
                self.logger.info(f"Screenshot saved to {screenshot_path}")
                
                # Log page source snippet
                page_source = self.driver.page_source
                if page_source:
                    self.logger.info(f"Page source (first 500 chars): {page_source[:500]}")
                raise
            
            # Enter phone number
            username_field = self.driver.find_element(By.NAME, 'uid')
            username_field.send_keys(KOTAK_PHONE_NUMBER)
            self.logger.info("Phone number entered")
            
            time.sleep(1)
            
            # Enter password
            password_field = self.driver.find_element(By.NAME, 'pwd')
            password_field.send_keys(KOTAK_PASSWORD)
            self.logger.info("Password entered")
            
            time.sleep(1)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'login')]")
            login_button.click()
            self.logger.info("Login button clicked")
            
            # Wait for dashboard to load
            time.sleep(3)
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'dashboard'))
            )
            
            self.logger.info("Successfully logged into Kotak Securities")
            return True
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")
