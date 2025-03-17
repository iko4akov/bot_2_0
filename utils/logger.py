# utils/logger.py

import json
from pathlib import Path
from aiologger import Logger
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.handlers.files import AsyncFileHandler
from aiologger.formatters.base import Formatter
from aiologger.levels import LogLevel


LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

LOG_LEVELS = {
    "DEBUG": LogLevel.DEBUG,
    "INFO": LogLevel.INFO,
    "WARNING": LogLevel.WARNING,
    "ERROR": LogLevel.ERROR,
    "CRITICAL": LogLevel.CRITICAL
}

async def setup_logger():
    """
    Настройка асинхронного логгера через JSON-конфигурацию.
    """
    config_path = Path("settings/logging_config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    logger_name = list(config["loggers"].keys())[0]
    logger_config = config["loggers"][logger_name]
    logger = Logger(name=logger_name, level=LOG_LEVELS[logger_config["level"].upper()])

    for handler_name in logger_config["handlers"]:
        handler_config = config["handlers"][handler_name]

        if handler_config["class"] == "aiologger.handlers.streams.AsyncStreamHandler":
            handler = AsyncStreamHandler()
        elif handler_config["class"] == "aiologger.handlers.files.AsyncFileHandler":
            handler = AsyncFileHandler(
                filename=handler_config["filename"],
                mode=handler_config.get("mode", "a"),
                encoding=handler_config.get("encoding", "utf-8")
            )
        else:
            raise ValueError(f"Неизвестный обработчик: {handler_config['class']}")

        handler.level = LOG_LEVELS[handler_config["level"].upper()]

        formatter = Formatter(handler_config["formatter"])
        handler.formatter = formatter

        logger.add_handler(handler)

    return logger
