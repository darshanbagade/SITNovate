import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scraper import fetch_reddit_reviews  # Import function to fetch Reddit reviews
from sentiment_analysis import get_sentiment
from preprocess import preprocess_text

# Streamlit UI
st.title("Real-Time Sentiment Analysis for Reddit Product Reviews")

# Input field for product name
product = st.text_input("Enter a product name to fetch Reddit reviews:")

if product:
    with st.spinner("Fetching Reddit reviews... Please wait."):
        reviews = fetch_reddit_reviews(product, limit=10)  # Fetch reviews from Reddit

    if not reviews:
        st.error("No reviews found for this product on Reddit.")
    else:
        # Convert reviews to DataFrame
        df = pd.DataFrame(reviews, columns=["review"])
        df["cleaned_review"] = df["review"].apply(preprocess_text)
        df["Sentiment"] = df["cleaned_review"].apply(get_sentiment)

        st.write("Processed Reddit Reviews:")
        st.dataframe(df.head(5))  # Show first 5 reviews

        sentiment_counts = df["Sentiment"].value_counts()

        # Pie Chart
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["green", "red", "blue"])
        ax.set_title("Sentiment Distribution")
        st.pyplot(fig)

        # Bar Chart
        st.subheader("Sentiment Count")
        fig, ax = plt.subplots()
        ax.bar(sentiment_counts.index, sentiment_counts.values, color=["green", "red", "blue"])
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")
        ax.set_title("Sentiment Analysis Bar Chart")
        st.pyplot(fig)
