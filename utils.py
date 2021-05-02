import urllib3
from bs4 import BeautifulSoup

class Utils:

    def get_connect(url: str):
        http = urllib3.PoolManager()
        try:
            r = http.request('GET', rf"{url}")
        except http.exceptions.HTTPError as err:
            return err 
        
        return r.data

    def soup_connection(data, encode = 'utf-8'):
        try:
            soup = BeautifulSoup(data, 'html5lib', from_encoding=encode)
        except:
            print("Could not create BeautifulSoup object")
        
        if not soup:
            print("Could not create BeautifulSoup object")

        return soup

    def get_scrap_connection(url: str, encode = 'utf-8'):
        http = urllib3.PoolManager()
        try:
            r = http.request('GET', rf"{url}")    
            try:
                soup = BeautifulSoup(r.data, 'html5lib', from_encoding = encode)
            except:
                print("Could not create BeautifulSoup object")
            return soup
        except urllib3.exceptions.HTTPError as err:
            return err


print(Utils.get_scrap_connection("1ssadsa"))