import json
from datetime import datetime
from login import KotakLogin
from portfolio import PortfolioAnalyzer
from chart_analyzer import ChartAnalyzer
from logger import get_logger

logger = get_logger(__name__)

class KotakSecuritiesAnalyzer:
    def __init__(self):
        self.login = KotakLogin()
        self.portfolio_analyzer = None
        self.chart_analyzer = None
        self.analysis_results = []
    
    def run(self, symbols=None):
        """Main execution method."""
        try:
            logger.info("=" * 60)
            logger.info("Starting Kotak Securities Analysis")
            logger.info("=" * 60)
            
            # Step 1: Setup and Login
            logger.info("\n[STEP 1] Setting up WebDriver and logging in...")
            self.login.setup_driver()
            self.login.login()
            
            # Step 2: Navigate to Portfolio
            logger.info("\n[STEP 2] Navigating to portfolio...")
            self.portfolio_analyzer = PortfolioAnalyzer(self.login.driver)
            self.portfolio_analyzer.navigate_to_portfolio()
            
            # Step 3: Get Stock Positions
            logger.info("\n[STEP 3] Fetching stock positions...")
            positions = self.portfolio_analyzer.get_stock_positions()
            
            if not positions:
                logger.warning("No positions found in portfolio")
                return
            
            logger.info(f"\nFound {len(positions)} positions in portfolio:")
            for pos in positions:
                logger.info(f"  - {pos['symbol']}: {pos['quantity']} units @ {pos['current_price']}")
            
            # Step 4: Analyze Charts for Each Position
            logger.info("\n[STEP 4] Opening and analyzing candlestick charts...")
            self.chart_analyzer = ChartAnalyzer(self.login.driver)
            
            stocks_to_analyze = symbols if symbols else [pos['symbol'] for pos in positions[:3]]  # Limit to 3 for testing
            
            for symbol in stocks_to_analyze:
                try:
                    logger.info(f"\n--- Analyzing {symbol} ---")
                    position = self.portfolio_analyzer.get_position_by_symbol(symbol)
                    
                    if not position:
                        logger.warning(f"Position not found for {symbol}, skipping")
                        continue
                    
                    # Open chart
                    self.chart_analyzer.open_chart(symbol)
                    
                    # Set timeframe to hourly
                    self.chart_analyzer.set_timeframe('1H')
                    
                    # Analyze movement
                    analysis = self.chart_analyzer.analyze_current_movement()
                    
                    # Take screenshot
                    screenshot_file = f"chart_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    self.chart_analyzer.take_screenshot(screenshot_file)
                    
                    # Close chart
                    self.chart_analyzer.close_chart()
                    
                    # Store results
                    result = {
                        'symbol': symbol,
                        'position': position,
                        'analysis': analysis,
                        'screenshot': screenshot_file,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.analysis_results.append(result)
                    
                    logger.info(f"✓ Analysis complete for {symbol}")
                    
                except Exception as e:
                    logger.error(f"Failed to analyze {symbol}: {str(e)}")
                    continue
            
            # Step 5: Generate Report
            logger.info("\n[STEP 5] Generating analysis report...")
            self.generate_report()
            
            logger.info("\n" + "=" * 60)
            logger.info("Analysis Complete")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Fatal error in execution: {str(e)}")
            raise
        finally:
            # Cleanup
            if self.login:
                self.login.close()
    
    def generate_report(self):
        """Generate and save analysis report."""
        try:
            report_file = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_symbols_analyzed': len(self.analysis_results),
                'results': self.analysis_results
            }
            
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Report saved to {report_file}")
            
            # Print summary
            print("\n" + "=" * 60)
            print("ANALYSIS SUMMARY")
            print("=" * 60)
            for result in self.analysis_results:
                print(f"\n{result['symbol']}:")
                print(f"  Position: {result['position']['quantity']} units @ {result['position']['current_price']}")
                print(f"  Trend: {result['analysis'].get('trend', 'N/A')}")
                print(f"  Current Price: {result['analysis'].get('current_price', 'N/A')}")
                print(f"  Chart Screenshot: {result['screenshot']}")
            print("=" * 60)
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")


if __name__ == '__main__':
    analyzer = KotakSecuritiesAnalyzer()
    
    # Run analysis for all positions or specific symbols
    # analyzer.run(symbols=['RELIANCE', 'TCS', 'INFY'])  # Analyze specific stocks
    analyzer.run()  # Analyze all positions
