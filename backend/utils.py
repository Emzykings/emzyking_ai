def extract_keywords(messages: list[str]) -> str:
    """
    Basic fallback summarizer: Extract key phrases from the most recent messages.
    """
    if not messages:
        return "Untitled Chat"

    # Combine and tokenize the last 5–10 messages
    text = " ".join(messages[-10:])
    words = [w.strip(".,!?()[]") for w in text.lower().split() if len(w) > 3]
    
    # Get unique words (naive summary)
    keywords = list(set(words))[:5]
    return ", ".join(keywords).title() or "Untitled Chat"
