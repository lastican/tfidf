import re
import math
from collections import Counter

def clean_text(text):
    """Remove special characters and convert to lowercase"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def calculate_tf_idf(text):
    """
    Calculate TF-IDF for words in the text
    
    TF (Term Frequency): Count of word in text
    IDF (Inverse Document Frequency): Log of (total sentences / sentences containing the word)
    """
    cleaned_text = clean_text(text)
    
    # Split into words and sentences
    words = cleaned_text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    word_counts = Counter(words)
    
    # using sentences as documents
    word_in_sentences = {}
    for word in set(words):
        word_in_sentences[word] = sum(1 for sentence in sentences if word.lower() in clean_text(sentence))
    
    tf_idf_scores = {}
    for word, count in word_counts.items():
        if len(word) <= 1:  # Skip single characters
            continue
        
        tf = count
        idf = math.log(len(sentences) / word_in_sentences[word]) if word_in_sentences[word] > 0 else 0
        tf_idf_scores[word] = {
            'word': word,
            'tf': tf,
            'idf': round(idf, 4)
        }
    
    return list(tf_idf_scores.values())