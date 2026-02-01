"""
Reddit scraper module for fetching stock-related posts
"""
import praw
import os
from dotenv import load_dotenv
from datetime import datetime
import re

# Load environment variables
load_dotenv()


class RedditScraper:
    """Scrapes Reddit for stock mentions and discussions"""
    
    def __init__(self):
        """Initialize Reddit API connection"""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'StockSentimentAnalyzer/1.0')
        )
        
    def extract_stock_tickers(self, text):
        """
        Extract stock ticker symbols from text
        Looks for $SYMBOL or uppercase words 2-5 characters long
        """
        tickers = set()
        
        # Pattern 1: $SYMBOL format
        dollar_tickers = re.findall(r'\$([A-Z]{1,5})\b', text)
        tickers.update(dollar_tickers)
        
        # Pattern 2: Uppercase words (2-5 chars) that might be tickers
        # Exclude common words
        common_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                       'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET',
                       'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW',
                       'OLD', 'SEE', 'TWO', 'WHO', 'BOY', 'DID', 'ITS', 'LET',
                       'PUT', 'SAY', 'SHE', 'TOO', 'USE', 'WSB', 'CEO', 'IPO',
                       'ETF', 'ATH', 'IMO', 'YOLO', 'DD', 'TLDR', 'TL;DR'}
        
        word_tickers = re.findall(r'\b[A-Z]{2,5}\b', text)
        word_tickers = [t for t in word_tickers if t not in common_words]
        tickers.update(word_tickers)
        
        return list(tickers)
    
    def scrape_subreddit(self, subreddit_name, limit=100, time_filter='day', 
                        min_score=10, min_comments=5):
        """
        Scrape posts from a specific subreddit
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Number of posts to fetch
            time_filter: Time period ('hour', 'day', 'week', 'month', 'year', 'all')
            min_score: Minimum upvotes
            min_comments: Minimum number of comments
            
        Returns:
            List of post dictionaries
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for post in subreddit.hot(limit=limit):
                # Filter by score and comments
                if post.score < min_score or post.num_comments < min_comments:
                    continue
                
                # Extract stock tickers
                full_text = f"{post.title} {post.selftext}"
                tickers = self.extract_stock_tickers(full_text)
                
                post_data = {
                    'subreddit': subreddit_name,
                    'title': post.title,
                    'text': post.selftext,
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'url': post.url,
                    'author': str(post.author),
                    'tickers': tickers,
                    'upvote_ratio': post.upvote_ratio,
                }
                
                posts.append(post_data)
                
            return posts
            
        except Exception as e:
            print(f"Error scraping r/{subreddit_name}: {str(e)}")
            return []
    
    def scrape_multiple_subreddits(self, subreddit_list, limit=100, 
                                   time_filter='day', min_score=10, min_comments=5):
        """
        Scrape multiple subreddits
        
        Returns:
            Dictionary mapping subreddit names to lists of posts
        """
        all_posts = {}
        
        for subreddit in subreddit_list:
            print(f"Scraping r/{subreddit}...")
            posts = self.scrape_subreddit(
                subreddit, 
                limit=limit,
                time_filter=time_filter,
                min_score=min_score,
                min_comments=min_comments
            )
            all_posts[subreddit] = posts
            print(f"  Found {len(posts)} relevant posts")
            
        return all_posts
