"""
Main agent for Reddit Stock Sentiment Analysis
"""
import os
import sys
from datetime import datetime
import json

from reddit_scraper import RedditScraper
from sentiment_analyzer import SentimentAnalyzer
from news_scraper import NewsScraper
from config import SUBREDDITS, POST_LIMIT, TIME_FILTER, MIN_SCORE, MIN_COMMENTS


class StockSentimentAgent:
    """Main agent that coordinates scraping, analysis, and reporting"""
    
    def __init__(self):
        """Initialize all components"""
        self.reddit_scraper = RedditScraper()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.news_scraper = NewsScraper()
        
    def analyze_reddit_stocks(self, subreddits=None, limit=None, min_mentions=3):
        """
        Main analysis pipeline
        
        Args:
            subreddits: List of subreddit names (uses config default if None)
            limit: Number of posts per subreddit (uses config default if None)
            min_mentions: Minimum mentions for a stock to be included in results
            
        Returns:
            Dictionary with analysis results
        """
        # Use defaults from config if not provided
        if subreddits is None:
            subreddits = SUBREDDITS
        if limit is None:
            limit = POST_LIMIT
            
        print("=" * 80)
        print("REDDIT STOCK SENTIMENT ANALYZER")
        print("=" * 80)
        print(f"\nAnalyzing {len(subreddits)} subreddits: {', '.join(subreddits)}")
        print(f"Fetching up to {limit} posts per subreddit")
        print(f"Time filter: {TIME_FILTER}")
        print(f"Minimum score: {MIN_SCORE}, Minimum comments: {MIN_COMMENTS}")
        print("\n" + "-" * 80)
        
        # Step 1: Scrape Reddit
        print("\n[1/4] Scraping Reddit posts...")
        all_posts = self.reddit_scraper.scrape_multiple_subreddits(
            subreddits,
            limit=limit,
            time_filter=TIME_FILTER,
            min_score=MIN_SCORE,
            min_comments=MIN_COMMENTS
        )
        
        # Flatten posts
        flat_posts = []
        for subreddit, posts in all_posts.items():
            flat_posts.extend(posts)
        
        print(f"Total posts collected: {len(flat_posts)}")
        
        # Step 2: Analyze sentiment
        print("\n[2/4] Analyzing sentiment...")
        analyzed_posts = self.sentiment_analyzer.analyze_posts(flat_posts)
        
        # Step 3: Aggregate by stock
        print("\n[3/4] Aggregating stock mentions...")
        stock_data = self.sentiment_analyzer.aggregate_stock_sentiment(analyzed_posts)
        
        print(f"Total unique tickers found: {len(stock_data)}")
        
        # Step 4: Rank stocks
        print("\n[4/4] Ranking stocks...")
        ranked_stocks = self.sentiment_analyzer.rank_stocks(stock_data, min_mentions=min_mentions)
        
        print(f"Stocks with at least {min_mentions} mentions: {len(ranked_stocks)}")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'subreddits_analyzed': subreddits,
            'total_posts': len(flat_posts),
            'total_tickers': len(stock_data),
            'ranked_stocks': ranked_stocks,
            'stock_data': stock_data
        }
    
    def get_news_for_top_stocks(self, ranked_stocks, top_n=10):
        """
        Fetch news for top ranked stocks
        
        Args:
            ranked_stocks: List of (ticker, data) tuples
            top_n: Number of top stocks to get news for
            
        Returns:
            Dictionary of news by ticker
        """
        print(f"\n" + "=" * 80)
        print(f"FETCHING NEWS FOR TOP {top_n} STOCKS")
        print("=" * 80)
        
        top_tickers = [ticker for ticker, _ in ranked_stocks[:top_n]]
        news_data = self.news_scraper.get_news_for_stocks(top_tickers)
        
        return news_data
    
    def print_report(self, analysis_results, news_data=None):
        """
        Print a formatted report of the analysis
        
        Args:
            analysis_results: Results from analyze_reddit_stocks
            news_data: Optional news data from get_news_for_top_stocks
        """
        print("\n" + "=" * 80)
        print("ANALYSIS REPORT")
        print("=" * 80)
        print(f"\nTimestamp: {analysis_results['timestamp']}")
        print(f"Subreddits: {', '.join(analysis_results['subreddits_analyzed'])}")
        print(f"Total posts analyzed: {analysis_results['total_posts']}")
        print(f"Total tickers found: {analysis_results['total_tickers']}")
        
        print("\n" + "=" * 80)
        print("TOP STOCKS BY SENTIMENT AND POPULARITY")
        print("=" * 80)
        
        ranked_stocks = analysis_results['ranked_stocks']
        
        if not ranked_stocks:
            print("\nNo stocks found with sufficient mentions.")
            return
        
        # Print top 20 stocks
        print(f"\n{'Rank':<6}{'Ticker':<10}{'Mentions':<10}{'Avg Sentiment':<15}{'Class':<12}{'Score':<10}")
        print("-" * 80)
        
        for i, (ticker, data) in enumerate(ranked_stocks[:20], 1):
            print(f"{i:<6}{ticker:<10}{data['mentions']:<10}"
                  f"{data['avg_sentiment']:>14.3f}{data['sentiment_class']:<12}"
                  f"{data['rank_score']:>9.2f}")
        
        # Print detailed info for top 5
        print("\n" + "=" * 80)
        print("DETAILED INFO - TOP 5 STOCKS")
        print("=" * 80)
        
        for i, (ticker, data) in enumerate(ranked_stocks[:5], 1):
            print(f"\n{i}. {ticker}")
            print(f"   Mentions: {data['mentions']}")
            print(f"   Average Sentiment: {data['avg_sentiment']:.3f} ({data['sentiment_class']})")
            print(f"   Positive/Neutral/Negative: {data['positive']}/{data['neutral']}/{data['negative']}")
            print(f"   Total upvotes: {data['total_score']}")
            print(f"   Total comments: {data['total_comments']}")
            print(f"   Rank score: {data['rank_score']:.2f}")
            
            # Top posts
            print(f"   Top posts:")
            for post in sorted(data['posts'], key=lambda x: x['score'], reverse=True)[:3]:
                print(f"      - [{post['subreddit']}] {post['title'][:60]}... "
                      f"(score: {post['score']}, sentiment: {post['sentiment']:.2f})")
        
        # Print news if available
        if news_data:
            print("\n" + "=" * 80)
            print("NEWS AND INFORMATION SOURCES")
            print("=" * 80)
            
            for ticker, news_items in news_data.items():
                print(f"\n{ticker}:")
                for item in news_items:
                    print(f"   [{item['source']}] {item['url']}")
                    if 'note' in item:
                        print(f"      Note: {item['note']}")
    
    def save_results(self, analysis_results, news_data=None, filename=None):
        """
        Save results to a JSON file
        
        Args:
            analysis_results: Results from analyze_reddit_stocks
            news_data: Optional news data
            filename: Output filename (default: results_TIMESTAMP.json)
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"results_{timestamp}.json"
        
        output = {
            'analysis': analysis_results,
            'news': news_data
        }
        
        # Convert ranked_stocks to serializable format
        output['analysis']['ranked_stocks'] = [
            {'ticker': ticker, 'data': data}
            for ticker, data in analysis_results['ranked_stocks']
        ]
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2, default=str)
        
        print(f"\n" + "=" * 80)
        print(f"Results saved to: {filename}")
        print("=" * 80)


def main():
    """Main entry point"""
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("ERROR: .env file not found!")
        print("Please create a .env file with your Reddit API credentials.")
        print("See .env.example for the required format.")
        print("\nTo get Reddit API credentials:")
        print("1. Go to https://www.reddit.com/prefs/apps")
        print("2. Click 'Create App' or 'Create Another App'")
        print("3. Choose 'script' as the app type")
        print("4. Copy the client ID and secret to your .env file")
        sys.exit(1)
    
    # Create agent
    agent = StockSentimentAgent()
    
    # Run analysis
    print("\nStarting analysis...")
    results = agent.analyze_reddit_stocks(min_mentions=3)
    
    # Get news for top stocks
    news = agent.get_news_for_top_stocks(results['ranked_stocks'], top_n=10)
    
    # Print report
    agent.print_report(results, news)
    
    # Save results
    agent.save_results(results, news)
    
    print("\nAnalysis complete!")


if __name__ == '__main__':
    main()
