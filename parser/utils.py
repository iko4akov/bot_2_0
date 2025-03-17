from parser.config import stop_words, drop_word


async def check_stop_words(message: str):
    for word in stop_words:
        if word in message.lower():
            return False
    return True

async def drop_words(message: str) -> str:
    for bad_word in drop_word:
        message.replace(bad_word, "")

    return message
