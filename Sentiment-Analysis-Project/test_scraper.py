from scraper import fetch_reviews_api

product_url = "https://www.amazon.in/dp/B0CHX1W1XY"  
reviews = fetch_reviews_api(product_url)

print("Fetched Reviews:")
for review in reviews:
    print("-", review)
