from bs4 import BeautifulSoup
import urllib3

class Player:
    def __init__(self, character_name: str):
        self.__character_name = character_name
        self.__character_url = "https://www.tibia.com/community/?subtopic=characters"

    @property
    def character_name(self):
        return self.__character_name

    @character_name.setter
    def character_name(self, character_name):
        self.__character_name = character_name

    def __info_table(self, bs_char_table):
        values = bs_char_table.find_all('tr')
        info = []
        val = []
        for idx, value in enumerate(values):
            if (idx == 0) or (idx == 11):
                continue
            
            td_val = value.find_all('td')
            
            info.append(td_val[0].get_text().replace(u'\xa0', u' ').replace(':', '').strip())
            val.append(td_val[1].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip())

        return dict(zip(info, val))

    def __achievements_table(self, bs_achv_table):
        values = bs_achv_table.find_all('tr')
        star = []
        achv = []
        for idx,value in enumerate(values):
            if (idx == 0):
                continue
            td_val = value.find_all('td')
            if td_val[0].find_all('img'):
                ammount = len(td_val[0].find_all('img'))
                star.append(ammount*'*')
                achv.append(td_val[1].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip())
            else:
                star.append('0')
                achv.append(td_val[0].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip())

        return list(zip(star, achv))

    def __deaths_table(self, bs_dth_table):
        values = bs_dth_table.find_all('tr')
        time = []
        desc = []
        for idx,value in enumerate(values):
            if (idx == 0):
                continue
            td_val = value.find_all('td')
            time.append(td_val[0].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').replace(':', '').strip())
            desc.append(td_val[1].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip())

        return dict(zip(time, desc))

    def __account_table(self, bs_acc_table):
        values = bs_acc_table.find_all('tr')
        info = []
        desc = []
        for idx,value in enumerate(values):
            if (idx == 0):
                continue
            td_val = value.find_all('td')
            info.append(td_val[0].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').replace(':', '').strip())
            desc.append(td_val[1].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip())

        return dict(zip(info, desc))

    def __characters_table(self, bs_acc_char_table):
        values = bs_acc_char_table.find_all('tr')
        name = []
        world = []
        status = []
        for idx,value in enumerate(values):
            if (idx == 0) or (idx == 1):
                continue
            td_val = value.find_all('nobr')
            if not td_val:
                continue
            name.append(td_val[0].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').replace(':', '').strip())
            world.append(td_val[1].get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip())
            isonline = value.find('b', 'green')
            if isonline:
                status.append(isonline.get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip())
            else:
                status.append("offline")

        return list(zip(name,world,status))

    def get_player_info(self):
        http = urllib3.PoolManager()
        r = http.request('POST', self.__character_url, fields={'name': self.__character_name })
        soup = BeautifulSoup(r.data, 'html5lib', from_encoding="utf-8")

        content = soup.find('div', 'BoxContent')

        tables = content.find_all('table')
        character_info = tables[0]
        account_achievements = tables[1]

        if (tables[2].find('input')) or (not tables[2]) or (tables[2].find(text='Account Information')):
            char_deaths = "No deaths"
        else:
            char_deaths = self.__deaths_table(tables[2])

        char_info = self.__info_table(character_info)
        acc_achv = self.__achievements_table(account_achievements)

        if char_deaths == "No deaths":
            acc_info = self.__account_table(tables[2])
        elif (tables[3].find('input')) or (not tables[3]) or (char_deaths != "No deaths"):
            acc_info = "Not displayed"
        else:
            acc_info = self.__account_table(tables[3])

        if acc_info == "Not displayed":
            acc_characters = "Not displayed"
        else:
            if char_deaths == "No deaths":
                acc_characters = self.__characters_table(tables[3])
            else:
                acc_characters = self.__characters_table(tables[4])
        
            
        return {
            'Info': char_info,
            'Achievements': acc_achv,
            'Deaths': char_deaths,
            'Account_Info': acc_info,
            'Account_Characters': acc_characters
        }

    def get_player_single_info(self, info: str):
        return self.get_player_info()['Info'].get(info)

    @property
    def player_deaths(self):
        return self.get_player_info()['Deaths']

    @property
    def player_infos(self):
        return self.get_player_info()['Info']
    
    @property
    def player_achievements(self):
        return self.get_player_info()['Achievements']

    @property
    def player_account_info(self):
        return self.get_player_info()['Account_Info']

    @property
    def player_account_characters(self):
        return self.get_player_info()['Account_Characters']

player = Player('Critsix')
print(player.player_account_info)