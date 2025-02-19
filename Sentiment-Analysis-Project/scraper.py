import tweepy
import pandas as pd
import os
import time
from sentiment_analysis import get_sentiment
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_twitter_reviews(product_name, count=5):
    """Fetches recent tweets mentioning a product with optimized API usage."""
    
    query = f"{product_name} -is:retweet lang:en"

    try:
        response = client.search_recent_tweets(query=query, tweet_fields=["text"], max_results=count)

        if response.data:
            return [tweet.text for tweet in response.data]
        else:
            return ["No relevant tweets found."]

    except tweepy.TooManyRequests:
        print("Twitter API rate limit exceeded. Retrying in 30 seconds...")
        time.sleep(30)  # Wait before retrying
        return fetch_twitter_reviews(product_name, count)  # Retry the request

    except tweepy.TweepyException as e:
        return [f"Twitter API Error: {e}"]

# Example usage
if __name__ == "__main__":
    product = "iPhone 15"
    reviews = fetch_twitter_reviews(product, count=5)  # Fetch only 5 reviews to optimize speed
    df = pd.DataFrame(reviews, columns=["review"])
    df["Sentiment"] = df["review"].apply(get_sentiment)
    print(df.head())
