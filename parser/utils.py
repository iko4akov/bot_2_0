from settings.config import stop_words


def check_stop_words(message: str):
    for word in stop_words:
        if word in message.lower():
            return False
    return True
