import google.generativeai as genai

async def extract_keywords(messages: list[str]) -> str:
    """
    Generate a short AI-powered summary for a list of user messages.
    """
    if not messages:
        return "Untitled Chat"

    full_context = "\n".join(messages[:10])  # Use first 10 messages max

    prompt = (
        "Summarize this chat in 1 concise sentence as a title, using key technical topics only.\n\n"
        f"{full_context}\n\n"
        "Title Summary:"
    )

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return "Untitled Chat"