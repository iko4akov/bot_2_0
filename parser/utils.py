import re


async def remove_links(text: str) -> str:
    """
    Удаляет все ссылки из текста.
    """
    text = re.sub(r"@\w+", "", text)

    text = re.sub(r"http\S+", "", text)

    text = " ".join(text.split())

    return text
