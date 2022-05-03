import requests
import json


class GameData:
    game_data_json = None

    def __init__(self):
        GAME_DATA_URL = 'https://dsa.fan/api/game-data'
        try:
            r = requests.get(GAME_DATA_URL)
            if GameData.game_data_json == None:
                GameData.game_data_json = json.loads(r.text)
        except:
            pass

    @staticmethod
    def getJSON():
        r = requests.get(GameData.GAME_DATA_URL)
        return json.loads(r.text)

    def unitNameToNameKey(self, unitName):
        for key, value in GameData.game_data_json['strings'].items():
            if value == unitName and key.endswith('_UNIT_NAME'):
                return key

    def unitNameToID(self, unitName):
        nameKey = self.unitNameToNameKey(unitName)
        for unit in GameData.game_data_json['units'].values():
            if unit['NameKey'] == nameKey:
                return unit['ID']
    
    def nameKeyToUnitName(self, nameKey):
        return GameData.game_data_json['strings'][nameKey]

    def IDtoUnitNameKey(self, id):
        return GameData.game_data_json['units'][str(id)]['NameKey']
    
    def IDtoUnitName(self, id):
        return self.nameKeyToUnitName(self.IDtoUnitNameKey(id))
