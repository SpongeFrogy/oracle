from logging import Logger
from typing import Type


def log_raise(msg: str, logger: Logger, exeption: Type[Exception]):
    logger.error(msg)
    raise exeption(msg)