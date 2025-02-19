import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import string
from sentiment_analysis import get_sentiment  # Ensure correct import

# Function to clean text
def preprocess_text(text):
    if pd.isna(text) or not isinstance(text, str):  # Handle missing or non-string values
        return ""
    text = text.lower()  # Convert to lowercase
    text = "".join([char for char in text if char not in string.punctuation])  # Remove punctuation
    return text

# Streamlit UI
st.title("Customer Feedback Sentiment Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload a dataset (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert all column names to lowercase to avoid case-sensitive errors
    df.columns = df.columns.str.strip().str.lower()

    # Ensure 'review' column exists
    if 'review' not in df.columns:
        st.error("Error: The uploaded CSV must contain a 'review' column.")
        st.stop()  # Stop execution if column is missing

    # Apply text preprocessing
    df['cleaned_review'] = df['review'].apply(preprocess_text)

    # Apply Sentiment Analysis
    df['Sentiment'] = df['cleaned_review'].apply(get_sentiment)  # Now applying sentiment analysis correctly

    # Show Sample Data
    st.write("Sample Processed Data:")
    st.write(df.head())

    # Sentiment Count Visualization
    sentiment_counts = df['Sentiment'].value_counts()

    # Pie Chart
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["green", "red", "blue"])
    ax.set_title("Sentiment Distribution")
    st.pyplot(fig)

    # Bar Chart for Better Visualization
    st.subheader("Sentiment Count")
    fig, ax = plt.subplots()
    ax.bar(sentiment_counts.index, sentiment_counts.values, color=["green", "red", "blue"])
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Count")
    ax.set_title("Sentiment Analysis Bar Chart")
    st.pyplot(fig)
