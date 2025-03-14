import redis
import json


class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_cli = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def save_user_data(self, user_id: str, data: dict):
        """Сохраняет данные пользователя в Redis."""
        key = f"user:{user_id}"
        self.redis_cli.set(key, json.dumps(data))

    def get_user_data(self, user_id: str):
        """Получает данные пользователя из Redis."""
        key = f"user:{user_id}"
        data = self.redis_cli.get(key)
        return json.loads(data) if data else None

    def delete_user_data(self, user_id: str):
        """Удаляет данные пользователя из Redis."""
        key = f"user:{user_id}"
        self.redis_cli.delete(key)

    def save_session(self, user_id: str, session_data: dict):
        """Сохраняет сессию пользователя в Redis."""
        key = f"session:{user_id}"
        self.redis_cli.set(key, json.dumps(session_data))

    def get_session(self, user_id: str):
        """Получает сессию пользователя из Redis."""
        key = f"session:{user_id}"
        session_data = self.redis_cli.get(key)
        return json.loads(session_data) if session_data else None

    def delete_session(self, user_id: str):
        """Удаляет сессию пользователя из Redis."""
        key = f"session:{user_id}"
        self.redis_cli.delete(key)
