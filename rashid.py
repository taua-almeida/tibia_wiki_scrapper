from datetime import date
import pandas as pd 
from bs4 import BeautifulSoup
import urllib3

class Rashid:
    day_and_location = {
        "Monday": {
            "city": "Svargrond",
            "location": "http://www.whereisrashid.com/images/RashidSvarMon.png"
        },
        "Tuesday": {
            "city": "Liberty Bay",
            "location": "http://www.whereisrashid.com/images/RashidLBTues.png"
        },
        "Wednesday":{
            "city": "Port Hope",
            "location": "http://www.whereisrashid.com/images/RashidPHWed.png"
        },
        "Thursday":{
            "city": "Ankrahmun",
            "location": "http://www.whereisrashid.com/images/RashidAnkThurs.png"
        },
        "Friday": {
            "city": "Darashia",
            "location": "http://www.whereisrashid.com/images/RashidDaraFri.png"
        },
        "Saturday":{
            "city": "Edron",
            "location": "http://www.whereisrashid.com/images/RashidEdronSat.png"
        },
        "Sunday": {
            "city": "Carlin",
            "location": "http://www.whereisrashid.com/images/RashidCarSun.png"
        }
    }

    @staticmethod
    def where_is_rashid(day: str) -> dict:
        return Rashid.day_and_location.get(day)

    @staticmethod
    def where_is_rashid_today() -> dict:
        day = date.today().strftime("%A")
        return Rashid.day_and_location.get(day)

    def generate_items_and_values() -> dict:
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://www.tibiawiki.com.br/wiki/Rashid')
        soup = BeautifulSoup(r.data, 'html5lib', from_encoding="latin-1")
        all_tables = soup.find_all("table", "sortable")

        values = []
        items = []
        for table in all_tables:
            if table.find("td", "exception"):
                same_class = table.find("td", "exception")
                same_class['class'] = 'npcvalue'

            get_all_values = table.find_all("td", "npcvalue")
            for value in get_all_values:
                values.append(value.get_text().replace(u'\xa0', u' ').strip())
            get_all_items = table.find_all("span", "tooltip")
            for item in get_all_items:
                items.append(item.get_text().strip())

        return dict(zip(items, values))

    @staticmethod
    def what_rashid_buys() -> list:
        return list(Rashid.generate_items_and_values().keys())

    @staticmethod
    def how_much_rashid_pays(item: str) -> str:
        if not Rashid.generate_items_and_values().get(item):
            return f"Rashid does not buy this item ({item})"
        rashid_item_value = Rashid.generate_items_and_values()
        return f"Rashid pays: {rashid_item_value.get(item)} for the {item}"