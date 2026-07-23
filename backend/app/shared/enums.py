from enum import Enum


class SortDirection(int, Enum):
    ASC = 1
    DESC = -1


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"