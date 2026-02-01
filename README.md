# job-specific-resume-builder

This repository contains various tools and utilities:

## Stock Sentiment Analyzer

A Reddit-based stock sentiment analysis agent that helps identify trending stocks based on discussions in popular investment subreddits.

### Features
- Scrapes multiple investment-focused subreddits (r/wallstreetbets, r/stocks, r/investing, r/valueinvesting, etc.)
- Performs sentiment analysis using VADER
- Ranks stocks by sentiment and engagement
- Provides links to financial news sources
- Generates detailed reports in console and JSON format

### Quick Start

```bash
cd stock_sentiment_analyzer
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Reddit API credentials
python agent.py
```

For detailed documentation, see [stock_sentiment_analyzer/README.md](stock_sentiment_analyzer/README.md)

### Disclaimer
This tool is for educational purposes only and does not constitute financial advice.