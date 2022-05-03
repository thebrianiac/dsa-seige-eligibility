from unicodedata import name
import requests
import json
from GameData import GameData
import os
import datetime


class PlayerData:
    def __init__(self, id=None):
        self.api_key = ''
        self.game_data = GameData()
        self.id = id
        self.json = None

    def setAPIKey(self, key):
        self.api_key = key

    def loadJSON(self, file):
        with open(file, 'r') as f:
            self.json = json.load(f)

    def getJSON(self):
        PLAYER_DATA_URL = 'https://dsa.fan/api/players/'
        if self.json is None:
            if self.id:
                try:
                    self.loadJSON(os.path.join('cached', f'{self.id}.json'))
                    last_updated = datetime.datetime.fromtimestamp(self.json['updateTimestamp'])
                    stale_time = datetime.datetime.now() - last_updated
                    if stale_time.days == 0:
                        return self.json
                except:
                    pass

            try:
                r = requests.get(f'{PLAYER_DATA_URL}{self.id}', headers={'HTTP-X-API-IDENTIFIER':self.api_key})
                self.json = json.loads(r.text)
                self.json['updateTimestamp'] = datetime.datetime.now().timestamp()
            except:
                pass

        return self.json
    
    def getName(self):
        return self.getJSON()['player']['username']

    def getID(self):
        if self.id:
            return self.id
        else:
            return self.getJSON()['player']['id']

    def getUnits(self):
        units = self.getJSON()['player']['unitInventory']
        for unit in units:
            unit['name'] = self.game_data.IDtoUnitName(unit['definitionId'])
        return units
    
    def getUnitByID(self, unit_id):
        for unit in self.getUnits():
            if unit['definitionId'] == unit_id:
                return unit

    def getUnitByName(self, unit_name):
        return self.getUnitByID(self.game_data.unitNameToID(unit_name))

    def saveData(self, out_dir='cached'):
        self.getJSON()
        with open(os.path.join(out_dir, f'{self.getID()}.json'), 'w') as file:
            json.dump(self.json, file)

