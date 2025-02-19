import praw
import os
from dotenv import load_dotenv
import pandas as pd

# Load API credentials
load_dotenv()

# Reddit API Authentication
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_reddit_reviews(product_name, limit=10):
    """
    Fetch Reddit comments about a product from relevant subreddits.
    
    Parameters:
        product_name (str): The name of the product to search for.
        limit (int): The number of comments to fetch.
    
    Returns:
        list: A list of extracted comments.
    """
    reviews = []
    subreddit_list = ["technology", "gadgets", "Smartphones", "reviews"]

    for subreddit in subreddit_list:
        try:
            for post in reddit.subreddit(subreddit).search(product_name, limit=5):
                post.comments.replace_more(limit=0)  # Load all comments
                for comment in post.comments.list()[:limit]:  # Get top comments
                    reviews.append(comment.body)
                if len(reviews) >= limit:
                    return reviews[:limit]
        except Exception as e:
            return [f"Error fetching Reddit reviews: {e}"]

    return reviews if reviews else ["No relevant comments found on Reddit."]

# ✅ Example Usage
if __name__ == "__main__":
    product = "iPhone 15"
    reviews = fetch_reddit_reviews(product, limit=10)
    df = pd.DataFrame(reviews, columns=["review"])
    print(df.head())
