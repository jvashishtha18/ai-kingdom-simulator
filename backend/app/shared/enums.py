from enum import Enum


class SortDirection(int, Enum):
    ASC = 1
    DESC = -1


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"

class Role(str, Enum):
    PLAYER = 'PLAYER',
    ADMIN= 'ADMIN',
    MODERATOR = 'MODERATOR'
    AI_MASTER = 'AI_MASTER'


# Race Enum
# Using an enum prevents invalid values like:Human ,human,HUMANNN
class WorldRace(str, Enum):
    HUMAN = "HUMAN"
    ELF = "ELF"
    DWARF = "DWARF"
    ORC = "ORC"
