from bs4 import BeautifulSoup
import urllib3

class Traders:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __generates_just_buy(self, bs_table):
        values = []
        items = []

        for table in bs_table:

            if table.find("td", "exception"):
                same_class = table.find("td", "exception")
                same_class['class'] = 'npcvalue'

            get_all_values = table.find_all("td", "npcvalue")
            for value in get_all_values:
                value_to_append = value.get_text().replace(u'\xa0', u' ').strip()
                values.append(value_to_append)

            get_all_items = table.find_all("span", "tooltip")
            for item in get_all_items:
                item_to_append = item.get_text().strip()
                items.append(item_to_append)

        return dict(zip(items, values))

    def __generate_items_and_values(self) -> dict:
        http = urllib3.PoolManager()
        r = http.request('GET', rf"https://www.tibiawiki.com.br/wiki/{self.__name}")
        soup = BeautifulSoup(r.data, 'html5lib', from_encoding="latin-1")
        all_tables = soup.find_all("table", "sortable")
        
        if not all_tables:
            raise ValueError("Soup could not find table itens")        
        return self.__generates_just_buy(all_tables)

    def what_trader_buys(self) -> list:
        return list(self.__generate_items_and_values().keys())

    def how_much_trader_pays(self, item: str) -> str:
        if not self.__generate_items_and_values().get(item):
            return rf"{self.__name.title()} does not buy this item ({item})"
        trader_item_value = self.__generate_items_and_values()
        return rf"{self.__name.title()} pays: {trader_item_value.get(item)} for the {item}"

ysr = Traders('Yasir')
rsd = Traders('Rashid')
print(ysr.how_much_trader_pays("Zaogun Shoulderplates"))
print(rsd.how_much_trader_pays("Buckle"))
print(rsd.what_trader_buys())