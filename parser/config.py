from typing import List

from settings.config import API_ID, API_HASH


api_id: int = API_ID
api_hash: str = API_HASH

# Message answer
info_api_id: str = "Введите API_ID, получить его можете на сайте [my.telegram.org](https:/my.telegram.org)"

info_api_hash: str = "Введите API_HASH, получить его можно на сайте [my.telegram.org](https:/my.telegram.org)"

info_phone: str = "Введите телефон в формате +71234567890"

info_code: str = "Код отправлен. Введите его в формате: x1xx2x3x4x5\n" \
            "где 'x' это любой не числовой символ\n" \
            "Пример ваш код 11111\n" \
            "Ваше сообщение фыв1выу1fds1dsf1вфы1"

stop_words: list[str] = ["подписаться", "@", "https", "подпишись", "подписывайся", "подписка", "HTTPS", "https", "the экономист",
              "wildberries", "ozon", "реклама", "insider-t"]

target_channel: str = "@infa100go"

list_channels: List[str] = ["@kosmo_off", "@cosmosprosto", "@kosmos149"]
