import praw
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit API Credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_reddit_reviews(product_name, limit=10):
    """Fetches recent Reddit discussions mentioning a product."""
    reviews = []

    try:
        for submission in reddit.subreddit("all").search(product_name, limit=limit):
            if submission.selftext:
                reviews.append(submission.selftext[:500])  # Limiting text length
            else:
                reviews.append(submission.title)
        
        return reviews if reviews else ["No relevant reviews found."]
    
    except Exception as e:
        return [f"Error fetching reviews: {e}"]
