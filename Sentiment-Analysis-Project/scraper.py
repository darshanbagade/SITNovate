import praw
import os
from dotenv import load_dotenv

# Load Reddit API credentials from environment variables
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Authenticate Reddit API using PRAW
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_reddit_reviews(product_name, limit=10):
    """
    Fetches Reddit posts related to a product from r/reviews.
    
    Parameters:
        product_name (str): The product name to search for.
        limit (int): The number of posts to fetch.

    Returns:
        list: A list of review texts.
    """
    reviews = []
    
    try:
        for submission in reddit.subreddit("all").search(product_name, limit=limit):
            reviews.append(submission.title + " " + submission.selftext)

        return reviews if reviews else ["No reviews found."]
    
    except Exception as e:
        return [f"Error fetching reviews: {e}"]
