import pandas as pd
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

# Load dataset
df = pd.read_csv("D:\customer_reviews.csv")

# Preprocessing function
def preprocess(text):
    text = text.lower()  # Convert to lowercase
    text = "".join([char for char in text if char not in string.punctuation])  # Remove punctuation
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    return " ".join(words)

df['cleaned_review'] = df['review'].apply(preprocess)
df.head()

print(df.head())  # Display first 5 rows after preprocessing

df.to_csv("cleaned_reviews.csv", index=False)
print("✅ Preprocessed data saved successfully!")
