import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scraper import fetch_reddit_reviews
from sentiment_analysis import get_sentiment
from preprocess import preprocess_text

# Cache function to prevent multiple API calls
@st.cache_data(ttl=600)  # Cache results for 10 minutes
def get_reddit_reviews(product_name):
    return fetch_reddit_reviews(product_name, limit=10)  # Fetch 10 comments

# Streamlit UI
st.title("Real-Time Sentiment Analysis for Customer Feedback (Reddit)")

# Input for product name (Reddit reviews)
reddit_product = st.text_input("Enter product name for Reddit reviews:")

if reddit_product:
    with st.spinner("Fetching Reddit comments... Please wait."):
        reviews = get_reddit_reviews(reddit_product)  # Cached API request

    if not reviews or "No relevant comments found on Reddit." in reviews:
        st.error("No relevant comments found. Try another product.")
    else:
        df_reddit = pd.DataFrame(reviews, columns=["review"])
        df_reddit["cleaned_review"] = df_reddit["review"].apply(preprocess_text)
        df_reddit["Sentiment"] = df_reddit["cleaned_review"].apply(get_sentiment)

        st.write("Processed Reddit Reviews:")
        st.dataframe(df_reddit.head(5))  # Show first 5 reviews

        sentiment_counts = df_reddit["Sentiment"].value_counts()

        # Pie Chart
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["green", "red", "blue"])
        ax.set_title("Reddit Sentiment Distribution")
        st.pyplot(fig)

        # Bar Chart
        st.subheader("Sentiment Count")
        fig, ax = plt.subplots()
        ax.bar(sentiment_counts.index, sentiment_counts.values, color=["green", "red", "blue"])
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")
        ax.set_title("Sentiment Analysis Bar Chart")
        st.pyplot(fig)
