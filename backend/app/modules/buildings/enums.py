from enum import Enum

class BuildingStatus(str, Enum):
    UNDER_CONSTRUCTION = "under_construction"
    COMPLETED = "completed"
    UPGRADING = "upgrading"
    DESTROYED = "destroyed"
    
class BuildingType(str,Enum):
    TOWN_HALL = "town_hall"
    FARM = "farm"
    LUMBER_MILL = "lumber_mill"
    QUARRY = "quarry"
    IRON_MINE = "iron_mine"
    GOLD_MINE = "gold_mine"
    HOUSE = "house"
    BARRACKS = "barracks"