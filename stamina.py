from datetime import datetime, timedelta

class Stamina:
    def __init__(self, hour: int, minutes = 0, maxhour = 42, maxminutes = 0):
        self.__hour = hour
        self.__minutes = minutes
        self.__maxhour = maxhour
        self.__maxminutes = maxminutes

    @staticmethod
    def __transform_hour_to_minutes(h: int):
        return h*60

    @staticmethod
    def __generate_maxminutes(self) -> int:
        if self.__maxhour != 42:
            max_minutes = self.__transform_hour_to_minutes(self.__maxhour) + self.__maxminutes
        else:
            max_minutes = self.__transform_hour_to_minutes(self.__maxhour)

        return max_minutes

    def calculate(self) -> list:
        recived_minutes = self.__transform_hour_to_minutes(self.__hour) + self.__minutes
       
        max_minutes = self.__generate_maxminutes(self)
        
        diff6min = (max_minutes - recived_minutes) * 6
        diff3min = (max_minutes - recived_minutes) * 3

        return [str(timedelta(minutes=diff6min+10)), str(timedelta(minutes=diff3min))]
        


stamina1 = Stamina(39)
print(stamina1.calculate())