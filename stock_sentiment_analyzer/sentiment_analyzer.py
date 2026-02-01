"""
Sentiment analysis module for stock mentions
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict, Counter


class SentimentAnalyzer:
    """Analyzes sentiment of stock mentions in Reddit posts"""
    
    def __init__(self):
        """Initialize VADER sentiment analyzer"""
        self.analyzer = SentimentIntensityAnalyzer()
        
    def analyze_text(self, text):
        """
        Analyze sentiment of a text
        
        Returns:
            Dictionary with sentiment scores
        """
        scores = self.analyzer.polarity_scores(text)
        return scores
    
    def classify_sentiment(self, compound_score):
        """
        Classify sentiment based on compound score
        
        Args:
            compound_score: VADER compound score (-1 to 1)
            
        Returns:
            String classification: 'positive', 'neutral', or 'negative'
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_posts(self, posts):
        """
        Analyze sentiment for all posts
        
        Args:
            posts: List of post dictionaries
            
        Returns:
            Posts with added sentiment information
        """
        analyzed_posts = []
        
        for post in posts:
            full_text = f"{post['title']} {post['text']}"
            sentiment = self.analyze_text(full_text)
            
            post['sentiment'] = sentiment
            post['sentiment_class'] = self.classify_sentiment(sentiment['compound'])
            analyzed_posts.append(post)
            
        return analyzed_posts
    
    def aggregate_stock_sentiment(self, posts):
        """
        Aggregate sentiment by stock ticker
        
        Args:
            posts: List of analyzed posts
            
        Returns:
            Dictionary with aggregated sentiment per ticker
        """
        stock_data = defaultdict(lambda: {
            'mentions': 0,
            'total_score': 0,
            'total_comments': 0,
            'sentiment_scores': [],
            'positive': 0,
            'neutral': 0,
            'negative': 0,
            'posts': []
        })
        
        for post in posts:
            for ticker in post.get('tickers', []):
                stock_data[ticker]['mentions'] += 1
                stock_data[ticker]['total_score'] += post['score']
                stock_data[ticker]['total_comments'] += post['num_comments']
                stock_data[ticker]['sentiment_scores'].append(post['sentiment']['compound'])
                
                # Count sentiment classes
                sentiment_class = post['sentiment_class']
                stock_data[ticker][sentiment_class] += 1
                
                # Store post info
                stock_data[ticker]['posts'].append({
                    'title': post['title'],
                    'subreddit': post['subreddit'],
                    'score': post['score'],
                    'sentiment': post['sentiment']['compound'],
                    'url': post.get('url', '')
                })
        
        # Calculate average sentiment for each stock
        for ticker, data in stock_data.items():
            if data['sentiment_scores']:
                data['avg_sentiment'] = sum(data['sentiment_scores']) / len(data['sentiment_scores'])
                data['sentiment_class'] = self.classify_sentiment(data['avg_sentiment'])
            else:
                data['avg_sentiment'] = 0
                data['sentiment_class'] = 'neutral'
                
        return dict(stock_data)
    
    def rank_stocks(self, stock_data, min_mentions=3):
        """
        Rank stocks by sentiment and popularity
        
        Args:
            stock_data: Aggregated stock sentiment data
            min_mentions: Minimum mentions to be included in ranking
            
        Returns:
            Sorted list of (ticker, data) tuples
        """
        # Filter stocks with minimum mentions
        filtered_stocks = {
            ticker: data 
            for ticker, data in stock_data.items() 
            if data['mentions'] >= min_mentions
        }
        
        # Calculate a combined score (sentiment * log(mentions + engagement))
        import math
        
        for ticker, data in filtered_stocks.items():
            # Normalize sentiment from [-1, 1] to [0, 1]
            normalized_sentiment = (data['avg_sentiment'] + 1) / 2
            
            # Calculate engagement score
            engagement = data['total_score'] + data['total_comments']
            engagement_score = math.log(engagement + 1)
            
            # Combined score
            data['rank_score'] = normalized_sentiment * engagement_score
        
        # Sort by rank score
        ranked = sorted(
            filtered_stocks.items(),
            key=lambda x: x[1]['rank_score'],
            reverse=True
        )
        
        return ranked
