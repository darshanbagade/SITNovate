import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sentiment_analysis import get_sentiment
from preprocess import preprocess_text
from scraper import fetch_twitter_reviews

# Streamlit UI
st.title("Real-Time Sentiment Analysis for Customer Feedback")

# File uploader (CSV Input)
uploaded_file = st.file_uploader("Upload a dataset (CSV)", type=["csv"])

# Twitter product name input
twitter_product = st.text_input("Enter product name for Twitter reviews:")

# Create an empty DataFrame to store all reviews
all_reviews = pd.DataFrame(columns=["review"])

# Step 1: Process Uploaded CSV File
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()  # Standardize column names

        if "review" not in df.columns:
            st.error("Error: The uploaded CSV must contain a 'review' column.")
        else:
            df["cleaned_review"] = df["review"].apply(preprocess_text)
            df["Sentiment"] = df["cleaned_review"].apply(get_sentiment)
            all_reviews = pd.concat([all_reviews, df], ignore_index=True)

    except Exception as e:
        st.error(f"Error processing file: {e}")

# Step 2: Fetch Twitter Reviews
if twitter_product:
    with st.spinner("Fetching recent tweets... Please wait."):
        tweets = fetch_twitter_reviews(twitter_product, count=10)  # Reduce count to avoid rate limit

    if not tweets or "Error" in tweets[0]:
        st.error(tweets[0])
    else:
        df_tweets = pd.DataFrame(tweets, columns=["review"])
        df_tweets["cleaned_review"] = df_tweets["review"].apply(preprocess_text)
        df_tweets["Sentiment"] = df_tweets["cleaned_review"].apply(get_sentiment)
        all_reviews = pd.concat([all_reviews, df_tweets], ignore_index=True)

# Step 3: Display Sentiment Analysis
if not all_reviews.empty:
    st.subheader("Processed Reviews")
    st.dataframe(all_reviews.head(10))  # Show first 10 reviews

    # Sentiment Count
    sentiment_counts = all_reviews["Sentiment"].value_counts()

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

else:
    st.info("Please upload a CSV file or enter a product name to analyze sentiment.")
