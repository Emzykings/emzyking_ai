from collections import Counter
import re

def extract_keywords(messages, top_n=3):
    """
    Extracts the most frequent keywords from a list of user messages.
    """
    stopwords = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'in', 'to', 'for', 'and', 'with', 'of', 'you', 'your'}
    words = []

    # Concatenate all messages and split into words
    for message in messages:
        words += re.findall(r'\b\w+\b', message.lower())

    # Filter out stopwords and short words
    filtered_words = [word for word in words if word not in stopwords and len(word) > 2]

    # Count word frequency
    word_counts = Counter(filtered_words)

    # Get top N keywords
    most_common = [word for word, count in word_counts.most_common(top_n)]

    return ', '.join(most_common) if most_common else 'Untitled Chat'
