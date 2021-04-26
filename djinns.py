from bs4 import BeautifulSoup
import urllib3

class Djinns:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __generates_sell_and_buy(self, bs_table):
        values_to_buy = []
        items_to_buy = []
        values_to_sell = []
        items_to_sell = []
        flag_special_item = True if len(bs_table) == 3 else False

        for idx,table in enumerate(bs_table):
 
            if table.find("td", "exception"):
                same_class = table.find("td", "exception")
                same_class['class'] = 'npcvalue'

            get_all_values = table.find_all("td", "npcvalue")
            for value in get_all_values:
                value_to_append = value.get_text().replace(u'\xa0', u' ').strip()
                if flag_special_item:
                    values_to_sell.append(value_to_append) if (idx == 0) or (idx == 1) else values_to_buy.append(value_to_append)
                else:
                    values_to_sell.append(value_to_append) if idx == 0 else values_to_buy.append(value_to_append)

            get_all_items = table.find_all("span", "tooltip")
            for item in get_all_items:
                item_to_append = item.get_text().strip()
                if flag_special_item:
                    items_to_sell.append(item_to_append) if (idx == 0) or (idx == 1) else items_to_buy.append(item_to_append)
                else:
                    items_to_sell.append(item_to_append) if idx == 0 else items_to_buy.append(item_to_append)


        return [dict(zip(items_to_sell, values_to_sell)), dict(zip(items_to_buy, values_to_buy))]

    def __generate_items_and_values(self) -> dict:
        http = urllib3.PoolManager()
        r = http.request('GET', rf"https://www.tibiawiki.com.br/wiki/{self.__name}")
        soup = BeautifulSoup(r.data, 'html5lib', from_encoding="latin-1")
        all_tables = soup.find_all("table", "sortable")
        
        if not all_tables:
            raise ValueError("Soup could not find table itens")     
        ''' index 0 are itens that the npc sells and 1 are itens that the npc buys '''   
        return self.__generates_sell_and_buy(all_tables)

    
    def list_of_items(self) -> list:
        return self.__generate_items_and_values()

    def what_djinns_sells(self) -> list:
        return list(self.__generate_items_and_values()[0].keys())

    def what_djinns_buys(self) -> list:
        return list(self.__generate_items_and_values()[1].keys())

    def how_much_djinns_pays(self, item: str) -> str:
        if not self.__generate_items_and_values()[1].get(item):
            return rf"{self.__name.title()} does not buy this item ({item})"
        djinn_item_value = self.__generate_items_and_values()[1]
        return rf"{self.__name.title()} pays: {djinn_item_value.get(item)} for the {item}"

    def how_much_djinns_sells(self, item: str) -> str:
        if not self.__generate_items_and_values()[0].get(item):
            return rf"{self.__name.title()} does not sell this item ({item})"
        djinn_item_value = self.__generate_items_and_values()[0]
        return rf"{self.__name.title()} wants: {djinn_item_value.get(item)} for the {item}"

nbob = Djinns(r"Yaman")
print(nbob.how_much_djinns_pays('Underworld Rod'))