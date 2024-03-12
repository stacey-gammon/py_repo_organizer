from dataclasses import dataclass

from src.logger import Logger


@dataclass
class Ctx:
    logger: Logger
