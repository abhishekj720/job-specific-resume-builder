"""
News scraper module for fetching stock-related news
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class NewsScraper:
    """Scrapes financial news websites for stock information"""
    
    def __init__(self):
        """Initialize news scraper"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_yahoo_finance(self, ticker):
        """
        Search Yahoo Finance for stock news
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            List of news items
        """
        news_items = []
        
        try:
            url = f"https://finance.yahoo.com/quote/{ticker}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # This is a simplified version - actual scraping would need to
                # adapt to Yahoo Finance's current HTML structure
                news_items.append({
                    'source': 'Yahoo Finance',
                    'ticker': ticker,
                    'url': url,
                    'status': 'success',
                    'note': 'Check the URL for latest news and stock price'
                })
            else:
                news_items.append({
                    'source': 'Yahoo Finance',
                    'ticker': ticker,
                    'url': url,
                    'status': 'error',
                    'note': f'HTTP {response.status_code}'
                })
                
        except Exception as e:
            news_items.append({
                'source': 'Yahoo Finance',
                'ticker': ticker,
                'status': 'error',
                'note': str(e)
            })
            
        return news_items
    
    def get_marketwatch_info(self, ticker):
        """
        Get stock info from MarketWatch
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            List of info items
        """
        info_items = []
        
        try:
            url = f"https://www.marketwatch.com/investing/stock/{ticker.lower()}"
            
            info_items.append({
                'source': 'MarketWatch',
                'ticker': ticker,
                'url': url,
                'status': 'link_provided',
                'note': 'Visit URL for detailed stock information and news'
            })
                
        except Exception as e:
            info_items.append({
                'source': 'MarketWatch',
                'ticker': ticker,
                'status': 'error',
                'note': str(e)
            })
            
        return info_items
    
    def get_news_for_stocks(self, tickers):
        """
        Get news for multiple stock tickers
        
        Args:
            tickers: List of stock ticker symbols
            
        Returns:
            Dictionary mapping tickers to news items
        """
        all_news = {}
        
        for ticker in tickers[:10]:  # Limit to top 10 to avoid too many requests
            print(f"Fetching news for {ticker}...")
            news = []
            
            # Yahoo Finance
            yahoo_news = self.search_yahoo_finance(ticker)
            news.extend(yahoo_news)
            
            # MarketWatch
            marketwatch_info = self.get_marketwatch_info(ticker)
            news.extend(marketwatch_info)
            
            all_news[ticker] = news
            
        return all_news
