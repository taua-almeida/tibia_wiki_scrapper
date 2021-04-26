import math

class PartyLevel:

    party_bonus = {
        "Same vocation": r'20%',
        "Two distinct vocations": r'30%',
        "Three distinct vocations": r'60%',
        "Four distinct vocations": r'100%'
    }

    def __init__(self, mylvl: int):
        self.__mylvl = mylvl
    
    def minimum_lvl(self) -> int:
        min_level = (2/3)*self.__highest_lvl
        return math.floor(min_level)
    
    def range_to_share(self) -> int:
        min_level = math.floor((2/3)*self.__mylvl) 
        max_level = math.floor((self.__mylvl) / (2/3))
        return [min_level if min_level >=1 else 1, max_level]


pt = PartyLevel(1)
print(pt.range_to_share())
print(PartyLevel.party_bonus)