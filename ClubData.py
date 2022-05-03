from bs4 import BeautifulSoup
import requests


class ClubData():
    def __init__(self, id):
        CLUB_DATA_URL = 'https://dsa.fan/guilds/'
        try:
            r = requests.get(f'{CLUB_DATA_URL}{id}')
        except:
            pass
        self.html_data = r.text

    def getPlayers(self):
        parser = BeautifulSoup(self.html_data, 'html.parser')
        table = parser.find('table', attrs={'id': 'players'})
        players = []
        for row in table.find_all('a'):
            players.append({'name': row.string, 'id': row['href'][-8:]})
        return players
