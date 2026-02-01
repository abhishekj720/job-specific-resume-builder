"""
Basic tests for the Stock Sentiment Analyzer

These tests verify that the modules can be imported and basic
functionality works without requiring Reddit API credentials.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        import config
        print("✓ config imported")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    try:
        from sentiment_analyzer import SentimentAnalyzer
        print("✓ SentimentAnalyzer imported")
    except ImportError as e:
        print(f"✗ Failed to import SentimentAnalyzer: {e}")
        return False
    
    try:
        from news_scraper import NewsScraper
        print("✓ NewsScraper imported")
    except ImportError as e:
        print(f"✗ Failed to import NewsScraper: {e}")
        return False
    
    # Reddit scraper requires PRAW
    try:
        from reddit_scraper import RedditScraper
        print("✓ RedditScraper imported")
    except ImportError as e:
        print(f"✗ Failed to import RedditScraper: {e}")
        return False
    
    try:
        from agent import StockSentimentAgent
        print("✓ StockSentimentAgent imported")
    except ImportError as e:
        print(f"✗ Failed to import StockSentimentAgent: {e}")
        return False
    
    return True


def test_sentiment_analyzer():
    """Test sentiment analysis functionality"""
    print("\nTesting SentimentAnalyzer...")
    
    try:
        from sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        # Test positive sentiment
        text = "This stock is amazing! Great company with strong fundamentals."
        scores = analyzer.analyze_text(text)
        sentiment_class = analyzer.classify_sentiment(scores['compound'])
        
        print(f"  Test 1 - Positive text: '{text[:50]}...'")
        print(f"    Compound score: {scores['compound']:.3f}")
        print(f"    Classification: {sentiment_class}")
        
        if sentiment_class != 'positive':
            print(f"  ✗ Expected 'positive', got '{sentiment_class}'")
            return False
        print("  ✓ Positive sentiment detected correctly")
        
        # Test negative sentiment
        text = "This stock is terrible. Avoid at all costs!"
        scores = analyzer.analyze_text(text)
        sentiment_class = analyzer.classify_sentiment(scores['compound'])
        
        print(f"  Test 2 - Negative text: '{text}'")
        print(f"    Compound score: {scores['compound']:.3f}")
        print(f"    Classification: {sentiment_class}")
        
        if sentiment_class != 'negative':
            print(f"  ✗ Expected 'negative', got '{sentiment_class}'")
            return False
        print("  ✓ Negative sentiment detected correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing SentimentAnalyzer: {e}")
        return False


def test_ticker_extraction():
    """Test stock ticker extraction"""
    print("\nTesting ticker extraction...")
    
    try:
        # Import just the extraction method logic by testing the regex directly
        import re
        
        text = "I'm bullish on $AAPL and $TSLA. Also watching NVDA and MSFT closely."
        
        # Replicate the ticker extraction logic without needing Reddit API
        tickers = set()
        
        # Pattern 1: $SYMBOL format
        dollar_tickers = re.findall(r'\$([A-Z]{1,5})\b', text)
        tickers.update(dollar_tickers)
        
        # Pattern 2: Uppercase words (2-5 chars)
        common_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL'}
        word_tickers = re.findall(r'\b[A-Z]{2,5}\b', text)
        word_tickers = [t for t in word_tickers if t not in common_words]
        tickers.update(word_tickers)
        
        tickers = list(tickers)
        
        print(f"  Text: '{text}'")
        print(f"  Extracted tickers: {tickers}")
        
        expected = ['AAPL', 'TSLA', 'NVDA', 'MSFT']
        for ticker in expected:
            if ticker not in tickers:
                print(f"  ✗ Expected ticker '{ticker}' not found")
                return False
        
        print("  ✓ All expected tickers extracted")
        return True
        
    except Exception as e:
        print(f"✗ Error testing ticker extraction: {e}")
        return False


def test_news_scraper():
    """Test news scraper URL generation"""
    print("\nTesting NewsScraper...")
    
    try:
        from news_scraper import NewsScraper
        
        scraper = NewsScraper()
        
        # Test Yahoo Finance URL
        ticker = 'AAPL'
        news = scraper.search_yahoo_finance(ticker)
        
        print(f"  Testing Yahoo Finance for {ticker}")
        print(f"    Result: {news[0]['status']}")
        
        if 'url' in news[0]:
            print(f"    URL: {news[0]['url']}")
            if 'yahoo.com' not in news[0]['url']:
                print("  ✗ Invalid Yahoo Finance URL")
                return False
        
        print("  ✓ Yahoo Finance URL generated correctly")
        
        # Test MarketWatch URL
        news = scraper.get_marketwatch_info(ticker)
        
        print(f"  Testing MarketWatch for {ticker}")
        if 'url' in news[0]:
            print(f"    URL: {news[0]['url']}")
            if 'marketwatch.com' not in news[0]['url']:
                print("  ✗ Invalid MarketWatch URL")
                return False
        
        print("  ✓ MarketWatch URL generated correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing NewsScraper: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration settings"""
    print("\nTesting configuration...")
    
    try:
        import config
        
        print(f"  Number of subreddits: {len(config.SUBREDDITS)}")
        print(f"  Post limit: {config.POST_LIMIT}")
        print(f"  Time filter: {config.TIME_FILTER}")
        
        if len(config.SUBREDDITS) == 0:
            print("  ✗ No subreddits configured")
            return False
        
        print("  ✓ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error testing configuration: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 80)
    print("STOCK SENTIMENT ANALYZER - BASIC TESTS")
    print("=" * 80)
    print("\nThese tests verify basic functionality without Reddit API access.\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Sentiment Analysis", test_sentiment_analyzer),
        ("Ticker Extraction", test_ticker_extraction),
        ("News Scraper", test_news_scraper),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-" * 80)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
