# Kotak Securities Analyzer

A Python-based automation tool to log into Kotak Securities, analyze your portfolio holdings, and review hourly candlestick charts with trend analysis.

## Features

✅ **Secure Login** - Automated authentication with Kotak Securities  
✅ **Portfolio Analysis** - Extract all stock positions and holdings  
✅ **Chart Analysis** - Open hourly candlestick charts for each stock  
✅ **Trend Detection** - Analyze bullish/bearish movements  
✅ **Screenshots** - Capture chart snapshots for reference  
✅ **Report Generation** - JSON report with complete analysis  
✅ **Logging** - Comprehensive logs of all operations  

## Project Structure

```
kotak-securities-analyzer/
├── main.py              # Main execution script
├── config.py            # Configuration and constants
├── logger.py            # Logging setup
├── login.py             # Kotak Securities login module
├── portfolio.py         # Portfolio navigation and extraction
├── chart_analyzer.py    # Chart analysis module
├── requirements.txt     # Python dependencies
├── .env                 # Credentials (create this file)
└── README.md            # This file
```

## Prerequisites

- Python 3.8+
- macOS, Linux, or Windows
- Google Chrome or Firefox browser
- Kotak Securities account with login credentials

## Installation

### 1. Clone or Download the Project

```bash
cd /Users/maha/Documents/ravi/kotak-securities-analyzer
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File for Credentials

Create a `.env` file in the project root with your Kotak Securities credentials:

```env
KOTAK_USERNAME=your_username
KOTAK_PASSWORD=your_password
```

**⚠️ Security Warning:** Never commit `.env` file to version control. Add it to `.gitignore`.

## Configuration

Edit `config.py` to customize:

- **Browser**: Chrome or Firefox (default: Chrome)
- **Headless Mode**: Run without UI (default: False)
- **Timeframe**: Chart timeframe (default: 1H for hourly)
- **Analysis Duration**: Time to analyze each chart in seconds (default: 300)
- **Thresholds**: Customize price change and volume thresholds

## Usage

### Run Full Analysis

```bash
python main.py
```

This will:
1. Login to Kotak Securities
2. Navigate to your portfolio
3. Extract all stock positions
4. Open hourly candlestick chart for each position
5. Analyze current price movement and trends
6. Generate a JSON report with results

### Analyze Specific Stocks

Edit `main.py` and modify the last line:

```python
analyzer.run(symbols=['RELIANCE', 'TCS', 'INFY'])
```

### Output Files

After running, the script generates:

- **`analysis_report_YYYYMMDD_HHMMSS.json`** - Complete analysis report
- **`chart_SYMBOL_YYYYMMDD_HHMMSS.png`** - Chart screenshots
- **`kotak_analyzer.log`** - Detailed execution logs

## Analysis Report Structure

```json
{
  "timestamp": "2025-12-29T12:00:00.000000",
  "total_symbols_analyzed": 3,
  "results": [
    {
      "symbol": "RELIANCE",
      "position": {
        "symbol": "RELIANCE",
        "quantity": "10",
        "current_price": "2950.50",
        "pnl": "+5.2%"
      },
      "analysis": {
        "current_price": "2950.50",
        "trend": "UPTREND",
        "open": "2940.00",
        "high": "2960.00",
        "low": "2935.00",
        "close": "2950.50",
        "price_change": "+10.50",
        "price_change_percent": "+0.36%"
      },
      "screenshot": "chart_RELIANCE_20251229_120000.png",
      "timestamp": "2025-12-29T12:00:00.000000"
    }
  ]
}
```

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'selenium'"
```bash
pip install -r requirements.txt
```

**Issue**: "No element found" errors
- The Kotak Securities website structure may have changed
- Update XPath selectors in `login.py`, `portfolio.py`, and `chart_analyzer.py`
- Open the website in a browser and inspect HTML elements

**Issue**: Login fails
- Verify credentials in `.env` file
- Check if 2FA is enabled on your account (may require manual intervention)
- Ensure you have network connectivity

**Issue**: Charts not loading
- Increase `EXPLICIT_WAIT` in `config.py` (default: 15 seconds)
- Some charts may load asynchronously; add delays in `chart_analyzer.py`

## Customization

### Add More Analysis Metrics

Edit `chart_analyzer.py`'s `analyze_current_movement()` method to extract:
- Support/Resistance levels
- RSI, MACD, Bollinger Bands
- Volume analysis
- Moving averages

### Store Data in Database

Modify `main.py` to save results to SQLite, PostgreSQL, or MongoDB instead of JSON.

### Add Alerts

Implement notification system (email, SMS, Telegram) for significant price movements.

## Legal Notice

⚠️ **Use at your own risk.** This tool is for personal portfolio analysis only. Ensure compliance with Kotak Securities' terms of service. Do not use for:
- Automated trading without explicit permission
- High-frequency access that may overload servers
- Any illegal activities

## Future Enhancements

- [ ] Multi-account support
- [ ] Real-time price alerts
- [ ] Technical indicator calculations
- [ ] Export to CSV/Excel
- [ ] Web dashboard for results
- [ ] Database integration
- [ ] Email notifications

## License

This project is provided as-is for educational purposes.

## Support

For issues or improvements, refer to the error logs in `kotak_analyzer.log` for detailed debugging information.
