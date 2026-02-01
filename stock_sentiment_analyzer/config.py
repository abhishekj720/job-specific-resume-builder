"""
Configuration settings for the Reddit Stock Sentiment Analyzer
"""

# Popular investment-related subreddits
SUBREDDITS = [
    'wallstreetbets',      # WSB - High risk, meme stocks
    'stocks',              # General stock discussions
    'investing',           # Long-term investment strategies
    'valueinvesting',      # Value investing approach
    'StockMarket',         # Stock market news and discussions
    'options',             # Options trading
    'pennystocks',         # Penny stock discussions
    'Daytrading',          # Day trading strategies
    'SecurityAnalysis',    # Deep dive analysis
    'Bogleheads',          # Index fund investing
]

# Reddit API credentials (to be set in .env file)
REDDIT_CLIENT_ID = ''
REDDIT_CLIENT_SECRET = ''
REDDIT_USER_AGENT = 'StockSentimentAnalyzer/1.0'

# Analysis settings
POST_LIMIT = 100  # Number of posts to fetch per subreddit
TIME_FILTER = 'day'  # Options: 'hour', 'day', 'week', 'month', 'year', 'all'
MIN_SCORE = 10  # Minimum upvotes to consider a post
MIN_COMMENTS = 5  # Minimum comments to consider a post

# News sources for additional context
NEWS_SOURCES = [
    'https://finance.yahoo.com',
    'https://www.cnbc.com/markets',
    'https://www.marketwatch.com',
]
