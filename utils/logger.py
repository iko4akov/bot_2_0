# utils/logger.py

import json
from pathlib import Path
from aiologger import Logger
from aiologger.handlers.stream import AsyncStreamHandler
from aiologger.handlers.files import AsyncFileHandler
from aiologger.formatters.base import Formatter


LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

async def setup_logger():
    """
    Настройка асинхронного логгера через JSON-конфигурацию.
    """
    config_path = Path("settings/logging_config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    logger_name = list(config["loggers"].keys())[0]
    print(logger_name)
    logger_config = config["loggers"][logger_name]
    logger = Logger(name=logger_name, level=logger_config["level"])

    for handler_name in logger_config["handlers"]:
        handler_config = config["handlers"][handler_name]

        if handler_config["class"] == "aiologger.handlers.stream.AsyncStreamHandler":
            handler = AsyncStreamHandler(level=handler_config["level"])
        elif handler_config["class"] == "aiologger.handlers.files.AsyncFileHandler":
            handler = AsyncFileHandler(
                filename=handler_config["filename"],
                mode=handler_config.get("mode", "a"),
                encoding=handler_config.get("encoding", "utf-8"),
                level=handler_config["level"]
            )
        else:
            raise ValueError(f"Неизвестный обработчик: {handler_config['class']}")

        formatter = Formatter(handler_config["formatter"])
        handler.formatter = formatter

        logger.add_handler(handler)

    return logger
