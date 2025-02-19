import string
import pandas as pd

def preprocess_text(text):
    """Cleans text by converting to lowercase, removing punctuation, and handling NaN values."""
    if pd.isna(text) or not isinstance(text, str):
        return ""
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    return text
