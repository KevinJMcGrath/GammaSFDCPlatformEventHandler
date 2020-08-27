from enum import Enum

from .client import MongoClient

class BuildStatus(Enum):
    Pending = 0
    InProgress = 1
    Complete = 2
    Failed = 3

DBClient = MongoClient.from_config()
