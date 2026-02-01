"""
Example usage of the Stock Sentiment Analyzer

This script demonstrates various ways to use the analyzer
"""

from agent import StockSentimentAgent
from reddit_scraper import RedditScraper
from sentiment_analyzer import SentimentAnalyzer


def example_basic_analysis():
    """Run a basic analysis with default settings"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Analysis")
    print("=" * 80)
    
    agent = StockSentimentAgent()
    results = agent.analyze_reddit_stocks(min_mentions=2)
    agent.print_report(results)
    
    return results


def example_custom_subreddits():
    """Analyze specific subreddits only"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Analyzing Specific Subreddits")
    print("=" * 80)
    
    agent = StockSentimentAgent()
    
    # Focus on WSB and stocks only
    results = agent.analyze_reddit_stocks(
        subreddits=['wallstreetbets', 'stocks'],
        limit=50,
        min_mentions=5
    )
    
    print(f"\nTop 5 stocks from WSB and r/stocks:")
    for i, (ticker, data) in enumerate(results['ranked_stocks'][:5], 1):
        print(f"{i}. {ticker}: {data['avg_sentiment']:.3f} sentiment, {data['mentions']} mentions")
    
    return results


def example_component_usage():
    """Use individual components separately"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Using Individual Components")
    print("=" * 80)
    
    # Step 1: Scrape Reddit
    print("\nScraping r/wallstreetbets...")
    scraper = RedditScraper()
    posts = scraper.scrape_subreddit('wallstreetbets', limit=30, min_score=50)
    print(f"Found {len(posts)} posts")
    
    # Step 2: Analyze sentiment
    print("\nAnalyzing sentiment...")
    analyzer = SentimentAnalyzer()
    analyzed_posts = analyzer.analyze_posts(posts)
    
    # Step 3: Aggregate by ticker
    print("\nAggregating by ticker...")
    stock_data = analyzer.aggregate_stock_sentiment(analyzed_posts)
    
    # Step 4: Rank
    print("\nRanking stocks...")
    ranked = analyzer.rank_stocks(stock_data, min_mentions=2)
    
    print(f"\nTop 10 stocks from r/wallstreetbets:")
    print(f"{'Ticker':<10}{'Mentions':<10}{'Sentiment':<12}{'Class'}")
    print("-" * 50)
    for ticker, data in ranked[:10]:
        print(f"{ticker:<10}{data['mentions']:<10}{data['avg_sentiment']:<12.3f}{data['sentiment_class']}")


def example_filter_positive_stocks():
    """Filter to show only stocks with positive sentiment"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Filtering for Positive Sentiment Only")
    print("=" * 80)
    
    agent = StockSentimentAgent()
    results = agent.analyze_reddit_stocks(min_mentions=3)
    
    # Filter for positive sentiment only
    positive_stocks = [
        (ticker, data) 
        for ticker, data in results['ranked_stocks']
        if data['sentiment_class'] == 'positive'
    ]
    
    print(f"\nFound {len(positive_stocks)} stocks with positive sentiment:")
    print(f"{'Ticker':<10}{'Mentions':<10}{'Sentiment':<12}{'Rank Score'}")
    print("-" * 50)
    for ticker, data in positive_stocks[:15]:
        print(f"{ticker:<10}{data['mentions']:<10}{data['avg_sentiment']:<12.3f}{data['rank_score']:.2f}")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("REDDIT STOCK SENTIMENT ANALYZER - EXAMPLES")
    print("=" * 80)
    print("\nThis script demonstrates different ways to use the analyzer.\n")
    
    try:
        # Example 1: Basic usage
        example_basic_analysis()
        
        # Example 2: Custom subreddits
        # example_custom_subreddits()
        
        # Example 3: Using components individually
        # example_component_usage()
        
        # Example 4: Filter by sentiment
        # example_filter_positive_stocks()
        
        print("\n" + "=" * 80)
        print("Examples completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your Reddit credentials")
        print("2. Installed all dependencies (pip install -r requirements.txt)")


if __name__ == '__main__':
    main()
