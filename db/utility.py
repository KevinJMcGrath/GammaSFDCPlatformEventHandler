from enum import Enum

class BuildStatus(Enum):
    Pending = 0
    InProgress = 1
    Complete = 2
    Failed = 3