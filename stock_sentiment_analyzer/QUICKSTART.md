# Quick Start Guide

Get up and running with the Reddit Stock Sentiment Analyzer in 5 minutes!

## Step 1: Install Dependencies

```bash
cd stock_sentiment_analyzer
pip install -r requirements.txt
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

## Step 2: Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click **"Create App"** or **"Create Another App"**
3. Fill in the form:
   - **name**: Stock Sentiment Analyzer (or any name you like)
   - **App type**: Select **"script"**
   - **description**: (optional)
   - **about url**: (optional)
   - **redirect uri**: http://localhost:8080
4. Click **"Create app"**
5. You'll see your app details:
   - **Client ID**: The string under "personal use script"
   - **Secret**: The string next to "secret"

## Step 3: Configure Your Credentials

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=StockSentimentAnalyzer/1.0
```

## Step 4: Run the Analyzer

```bash
python agent.py
```

The analyzer will:
- ✅ Scrape 10 investment subreddits
- ✅ Extract stock ticker mentions
- ✅ Perform sentiment analysis
- ✅ Rank stocks by popularity and sentiment
- ✅ Fetch news links
- ✅ Generate a detailed report
- ✅ Save results to a JSON file

## Example Output

```
================================================================================
REDDIT STOCK SENTIMENT ANALYZER
================================================================================

Analyzing 10 subreddits: wallstreetbets, stocks, investing, valueinvesting...
Fetching up to 100 posts per subreddit

[1/4] Scraping Reddit posts...
Scraping r/wallstreetbets...
  Found 87 relevant posts
Scraping r/stocks...
  Found 64 relevant posts
...

[2/4] Analyzing sentiment...
[3/4] Aggregating stock mentions...
Total unique tickers found: 127

[4/4] Ranking stocks...
Stocks with at least 3 mentions: 45

================================================================================
TOP STOCKS BY SENTIMENT AND POPULARITY
================================================================================

Rank  Ticker    Mentions  Avg Sentiment  Class       Score     
--------------------------------------------------------------------------------
1     NVDA      28        0.412          positive    9.23
2     AAPL      25        0.334          positive    8.91
3     TSLA      22        0.289          positive    8.45
...
```

## What's Next?

### Customize Your Analysis

Edit `config.py` to:
- Change which subreddits to analyze
- Adjust the number of posts to fetch
- Modify filtering criteria

### Run Examples

```bash
python example.py
```

See different ways to use the analyzer programmatically.

### View Detailed Results

Check the generated `results_TIMESTAMP.json` file for:
- Complete stock data
- All analyzed posts
- Sentiment scores
- News links

## Tips

- Run during market hours for more active discussions
- Increase `POST_LIMIT` in `config.py` for more comprehensive analysis
- Focus on specific subreddits by editing the `SUBREDDITS` list
- Lower `min_mentions` when running to see more stocks in results

## Troubleshooting

### "Invalid Reddit credentials"
- Double-check your client ID and secret in `.env`
- Make sure there are no extra spaces or quotes
- Verify your app is set to "script" type

### "No stocks found"
- Try lowering `min_mentions` parameter
- Increase `POST_LIMIT` to analyze more posts
- Change `TIME_FILTER` to 'week' for more data

### Rate Limiting
- Wait a few minutes if you hit rate limits
- Reduce the number of subreddits or post limit
- Don't run the analyzer too frequently

## Need Help?

See the full [README.md](README.md) for detailed documentation.

## Disclaimer

⚠️ This tool is for educational purposes only. It does not constitute financial advice. Always do your own research before making investment decisions.
