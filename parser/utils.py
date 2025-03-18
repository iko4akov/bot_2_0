import re

from parser.config import stop_words

async def remove_links(text: str) -> str:
    """Удаляет все ссылки из текста."""
    text = re.sub(r"\[.*?\]\(https?://t\.me/\S+\)", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"#\S+", "", text)
    text = " ".join(text.split())
    for word in stop_words:
        text = re.sub(re.escape(word), "", text.lower(), flags=re.IGNORECASE)
    return text


