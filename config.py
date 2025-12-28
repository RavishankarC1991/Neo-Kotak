import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Kotak Securities Credentials
KOTAK_PHONE_NUMBER = os.getenv('KOTAK_PHONE_NUMBER', 'your_phone_number')
KOTAK_PASSWORD = os.getenv('KOTAK_PASSWORD', 'your_password')

# Website URLs
KOTAK_LOGIN_URL = 'https://ntrade.kotaksecurities.com/Login'
KOTAK_PORTFOLIO_URL = 'https://ntrade.kotaksecurities.com/dashboard/holdings'

# Selenium Configuration
BROWSER = 'chrome'  # or 'firefox' or 'safari'
IMPLICIT_WAIT = 10  # seconds
EXPLICIT_WAIT = 15  # seconds
HEADLESS = False  # Set to True to run in headless mode

# Chart Analysis Configuration
TIMEFRAME = '1H'  # 1H for hourly
CHART_ANALYSIS_DURATION = 300  # seconds to analyze chart before closing

# Analysis Thresholds
PRICE_CHANGE_THRESHOLD = 0.5  # percentage
VOLUME_THRESHOLD = 1000000  # minimum volume

# Log Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'kotak_analyzer.log'
