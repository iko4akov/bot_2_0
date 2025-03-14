from database.models import Users
from utils import logger


async def check_data(user: Users):
    errors = {}
    if not user.api_id:
        errors['api_id'] = "Отсутствует API_ID"
    if not user.api_hash:
        errors['api_hash'] = "Отсутствует API_HASH"
    if not user.phone:
        errors['phone'] = "Отсутствует phone"
    if not len(user.channel) == 0:
        errors['Channel'] = "Список каналов пуст"

    if errors:
        logger.warning(f"Ошибки при проверки данных {errors}")
        return {"success": False, "errors": errors}

    return {"succes": True}

def validate_phone_number(phone: str) -> bool:
    return phone.startswith("+") and phone[1:].isdigit()
