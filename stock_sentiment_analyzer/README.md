# Reddit Stock Sentiment Analyzer

A Python-based agent that scrapes Reddit to identify the best stocks to invest in based on sentiment analysis of discussions in popular investment subreddits.

## Features

- **Multi-Subreddit Scraping**: Analyzes posts from popular investment subreddits including:
  - r/wallstreetbets (WSB)
  - r/stocks
  - r/investing
  - r/valueinvesting
  - r/StockMarket
  - r/options
  - r/pennystocks
  - r/Daytrading
  - r/SecurityAnalysis
  - r/Bogleheads

- **Stock Ticker Extraction**: Automatically identifies stock ticker symbols from posts
- **Sentiment Analysis**: Uses VADER sentiment analysis to determine positive/negative sentiment
- **Ranking System**: Ranks stocks based on a combination of:
  - Average sentiment score
  - Number of mentions
  - Post engagement (upvotes and comments)
- **News Integration**: Provides links to Yahoo Finance and MarketWatch for additional research
- **Detailed Reports**: Generates comprehensive reports with top stocks and their sentiment metrics

## Installation

### Prerequisites

- Python 3.7 or higher
- Reddit API credentials (free)

### Setup

1. **Install dependencies**:
   ```bash
   cd stock_sentiment_analyzer
   pip install -r requirements.txt
   ```

2. **Get Reddit API credentials**:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Fill in the required fields (name, redirect uri can be http://localhost:8080)
   - Copy the client ID (under the app name) and secret

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Reddit credentials:
   ```
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USER_AGENT=StockSentimentAnalyzer/1.0
   ```

## Usage

### Basic Usage

Run the agent with default settings:
```bash
python agent.py
```

This will:
1. Scrape the configured subreddits for recent posts
2. Extract stock ticker mentions
3. Perform sentiment analysis
4. Rank stocks by sentiment and popularity
5. Fetch news links for top stocks
6. Print a detailed report
7. Save results to a JSON file

### Configuration

Edit `config.py` to customize:

- **SUBREDDITS**: List of subreddits to scrape
- **POST_LIMIT**: Number of posts to fetch per subreddit (default: 100)
- **TIME_FILTER**: Time period for posts ('hour', 'day', 'week', 'month', 'year', 'all')
- **MIN_SCORE**: Minimum upvotes for a post to be considered (default: 10)
- **MIN_COMMENTS**: Minimum comments for a post to be considered (default: 5)

### Output

The agent produces:

1. **Console Report**: A detailed text report showing:
   - Top 20 stocks ranked by sentiment and engagement
   - Detailed analysis of top 5 stocks
   - Sample posts for each top stock
   - News source links

2. **JSON File**: A comprehensive JSON file (`results_TIMESTAMP.json`) containing:
   - All analyzed data
   - Stock rankings
   - Sentiment scores
   - Post details
   - News links

### Example Output

```
================================================================================
TOP STOCKS BY SENTIMENT AND POPULARITY
================================================================================

Rank  Ticker    Mentions  Avg Sentiment  Class       Score     
--------------------------------------------------------------------------------
1     AAPL      45        0.342          positive    8.42
2     TSLA      38        0.289          positive    7.91
3     NVDA      32        0.401          positive    7.65
4     MSFT      28        0.267          positive    7.12
5     AMD       25        0.198          positive    6.58
...
```

## How It Works

### 1. Reddit Scraping
The `RedditScraper` class uses the PRAW (Python Reddit API Wrapper) library to:
- Connect to Reddit's API
- Fetch hot posts from specified subreddits
- Extract post metadata (title, text, score, comments, etc.)
- Identify stock ticker symbols using regex patterns

### 2. Sentiment Analysis
The `SentimentAnalyzer` class uses VADER (Valence Aware Dictionary and sEntiment Reasoner):
- Analyzes the sentiment of post titles and content
- Calculates compound sentiment scores (-1 to 1)
- Classifies sentiment as positive, neutral, or negative
- Aggregates sentiment by stock ticker

### 3. Ranking Algorithm
Stocks are ranked using a combined score:
```python
rank_score = normalized_sentiment × log(engagement + 1)
```
Where:
- `normalized_sentiment` = (sentiment + 1) / 2, scaled from [0, 1]
- `engagement` = total_upvotes + total_comments

### 4. News Integration
The `NewsScraper` provides links to:
- Yahoo Finance for stock quotes and news
- MarketWatch for detailed stock information

## Modules

- **`agent.py`**: Main orchestrator that coordinates all components
- **`reddit_scraper.py`**: Handles Reddit API interactions and data extraction
- **`sentiment_analyzer.py`**: Performs sentiment analysis and stock ranking
- **`news_scraper.py`**: Fetches news links for stocks
- **`config.py`**: Configuration settings and constants

## Limitations and Considerations

1. **Not Financial Advice**: This tool is for educational and research purposes only. Always do your own research before making investment decisions.

2. **Reddit API Rate Limits**: Reddit's API has rate limits. The default settings respect these limits, but extensive scraping may be throttled.

3. **Sentiment Analysis Accuracy**: VADER is effective for social media text but may not capture all nuances, sarcasm, or context-specific meanings.

4. **Ticker Extraction**: The regex-based ticker extraction may produce false positives (common words) or miss some tickers.

5. **Market Hours**: The tool analyzes whatever is being discussed at the time of running, which may not reflect current market conditions.

6. **News Scraping**: Direct news scraping is limited due to website protections. The tool provides links for manual review.

## Advanced Usage

### Custom Analysis

You can use individual components programmatically:

```python
from reddit_scraper import RedditScraper
from sentiment_analyzer import SentimentAnalyzer

# Scrape specific subreddits
scraper = RedditScraper()
posts = scraper.scrape_subreddit('wallstreetbets', limit=50)

# Analyze sentiment
analyzer = SentimentAnalyzer()
analyzed = analyzer.analyze_posts(posts)
stock_data = analyzer.aggregate_stock_sentiment(analyzed)
ranked = analyzer.rank_stocks(stock_data, min_mentions=2)

for ticker, data in ranked[:10]:
    print(f"{ticker}: {data['avg_sentiment']:.3f} ({data['mentions']} mentions)")
```

### Filter by Subreddit

To analyze specific subreddits:

```python
from agent import StockSentimentAgent

agent = StockSentimentAgent()
results = agent.analyze_reddit_stocks(
    subreddits=['wallstreetbets', 'stocks'],
    limit=200,
    min_mentions=5
)
```

## Troubleshooting

### "ERROR: .env file not found!"
- Make sure you've created a `.env` file with your Reddit credentials
- Copy `.env.example` to `.env` and fill in your credentials

### "Invalid Reddit credentials"
- Double-check your client ID and secret in the `.env` file
- Ensure there are no extra spaces or quotes
- Verify your Reddit app is set to "script" type

### "No stocks found with sufficient mentions"
- Try lowering the `min_mentions` parameter
- Increase the `POST_LIMIT` in config.py
- Change `TIME_FILTER` to 'week' or 'month' for more posts

### Rate Limiting
- If you hit Reddit's rate limits, wait a few minutes and try again
- Reduce `POST_LIMIT` to scrape fewer posts
- Analyze fewer subreddits

## Future Enhancements

Potential improvements:
- Historical tracking of stock sentiment over time
- Integration with actual stock price data
- Machine learning models for better sentiment analysis
- Real-time monitoring and alerts
- Web dashboard for visualization
- Integration with more news sources
- Options and crypto analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and informational purposes only. It is not financial advice. Stock trading carries risk, and you should consult with a financial advisor before making investment decisions. The creators of this tool are not responsible for any financial losses incurred from using this software.
