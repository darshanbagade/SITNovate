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
