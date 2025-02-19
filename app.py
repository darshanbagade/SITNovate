import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import nltk


nltk.download('stopwords')

# Function to analyze sentiment
def get_sentiment(text):
    analysis = TextBlob(str(text))
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

# Streamlit UI
st.title("Customer Feedback Sentiment Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload a dataset (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Apply Sentiment Analysis
    df['Sentiment'] = df['review'].apply(get_sentiment)

    # Show Data
    st.write(df.head())

    # for Sentiment Count Visualization
    sentiment_counts = df['Sentiment'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["green", "red", "blue"])
    st.pyplot(fig)
