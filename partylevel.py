import math

class PartyLevel:
    def __init__(self, highest_lvl: int):
        self.__highest_lvl = highest_lvl
    
    def mininum_lvl(self) -> int:
        min_level = (2/3)*self.__highest_lvl
        return math.floor(min_level)

pt = PartyLevel(180)
print(pt.mininum_lvl())
