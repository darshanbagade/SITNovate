import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from scraper import fetch_reddit_reviews
from sentiment_analysis import get_sentiment
from preprocess import preprocess_text

# Set page config for better UI
st.set_page_config(page_title="Sentiment Analysis", layout="wide")

# Apply default theme
bg_color = "white"
text_color = "black"
btn_color = "#007BFF"

st.markdown(
    f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stButton>button {{
            background-color: {btn_color};
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option:", ["Analyze CSV File", "Fetch Reddit Reviews"])

# Layout
st.title("Real-Time Sentiment Analysis for Customer Feedback")
st.write("Analyze customer feedback from uploaded CSV files or fetch live reviews from Reddit.")

# Data Storage
all_reviews = pd.DataFrame(columns=["review"])

if option == "Analyze CSV File":
    uploaded_file = st.file_uploader("Upload a dataset (CSV)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()
        if "review" not in df.columns:
            st.error("Error: The uploaded CSV must contain a 'review' column.")
        else:
            df["cleaned_review"] = df["review"].apply(preprocess_text)
            df["Sentiment"] = df["cleaned_review"].apply(get_sentiment)
            all_reviews = df

elif option == "Fetch Reddit Reviews":
    product_name = st.text_input("Enter product name for Reddit reviews:")
    if product_name:
        with st.spinner("Fetching recent Reddit reviews... Please wait."):
            reviews = fetch_reddit_reviews(product_name, limit=10)
        if not reviews or "No relevant reviews found." in reviews:
            st.error("No relevant reviews found. Try another product.")
        else:
            df = pd.DataFrame(reviews, columns=["review"])
            df["cleaned_review"] = df["review"].apply(preprocess_text)
            df["Sentiment"] = df["cleaned_review"].apply(get_sentiment)
            all_reviews = df

# Display Data & Insights
if not all_reviews.empty:
    st.subheader("Processed Reviews")
    st.dataframe(all_reviews.head(10))
    sentiment_counts = all_reviews["Sentiment"].value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["green", "red", "blue"])
        st.pyplot(fig)
    
    with col2:
        st.subheader("Sentiment Bar Chart")
        fig, ax = plt.subplots()
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=["green", "red", "blue"], ax=ax)
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    
    st.subheader("Word Cloud of Reviews")
    wordcloud = WordCloud(width=800, height=400, background_color=bg_color).generate(' '.join(all_reviews["cleaned_review"]))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

else:
    st.info("Upload a CSV file or enter a product name to analyze sentiment.")
