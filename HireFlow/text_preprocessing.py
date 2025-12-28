import nltk
import string
import re
from nltk.corpus import stopwords

# nltk.download("stopwords")

# def clean_text(text):
#     text = text.lower()
#     text = text.translate(str.maketrans("", "", string.punctuation))
    
#     stop_words = set(stopwords.words("english"))
#     words = text.split()
    
#     filtered_words = [word for word in words if word not in stop_words]
#     return " ".join(filtered_words)

def clean_text(text):
    """
    General cleaning for TF-IDF similarity.
    Lowercase, remove extra spaces and line breaks.
    """
    text = text.lower()
    text = text.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    return text

def clean_text_for_skills(text):
    """
    Cleaning for skill extraction.
    Normalize case, remove punctuation (hyphens, commas, bullets), and strip common filler words
    such as 'experience' so entries like 'Git Experience' match 'Git'.
    """
    # Normalize whitespace and line breaks
    text = text.replace("\n", " ").replace("\r", " ")
    # Lowercase for case-insensitive matching
    text = text.lower()
    # Replace any character that is not alphanumeric, plus, or hash with a space
    text = re.sub(r"[^a-z0-9\s\+\#]", " ", text)
    # Remove common filler words that often follow skills
    filler_words = ["experience", "experiences", "skill", "skills", "knowledge", "proficient"]
    for fw in filler_words:
        text = re.sub(r"\b" + re.escape(fw) + r"\b", " ", text)
    # Collapse multiple spaces
    text = " ".join(text.split())
    return text
