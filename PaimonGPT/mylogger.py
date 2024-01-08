# *_*coding:utf-8 *_*
# @Author : YueMengRui
import logging
from types import FrameType
from typing import cast
from loguru import logger
from configs import LOG_DIR

logger.add(
    sink=f"{LOG_DIR}/{{time:YYYY-MM-DD}}.log",
    rotation="00:00",
    retention=30,
    mode="a+",
    # compression="zip",
    enqueue=True,
    backtrace=True,
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:MM:SS.SSS}|{level}|{name}:{function}:{line} - {message}"
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


LOGGER_NAMES = [name for name in logging.root.manager.loggerDict]
LOGGER_NAMES.extend(["uvicorn.asgi", "uvicorn.access"])

# change handler for default uvicorn logger
logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGER_NAMES:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler()]
    logging_logger.propagate = False
