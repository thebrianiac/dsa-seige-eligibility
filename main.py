from GameData import GameData
from PlayerData import PlayerData
from ClubData import ClubData
import json
import csv
import datetime
import time

CLUB_ID = None
API_KEY = None
CHOSEN = [
    'OLAF',
    'THE HORNED KING',
    'OOGIE BOOGIE',
    'SALLY',
    'JACK SKELLINGTON',
    'THE QUEEN OF HEARTS',
    'FROZONE',
    'MIKE WAZOWSKI',
    'MERLIN']

if __name__ == '__main__':

    if (API_KEY is None):
        API_KEY = input('Enter DSA.fan API key:')

    if (CLUB_ID is None):
        CLUB_ID = input('Enter Club ID:')

    club_data = []

    players = ClubData(CLUB_ID).getPlayers()
    for index, player in enumerate(players):
        print(f'Fetching player data ({index+1:2}/{len(players):2}) for {player["id"]}({player["name"]})')
        pd = PlayerData(player['id'])
        pd.setAPIKey(API_KEY)
        pd.saveData(out_dir='cached')
        chosenUnits = {}

        for chosen in CHOSEN:
            try:
                unit = pd.getUnitByName(chosen)
            except:
                print('ERROR: Unable to fetch. Sleeping for 2 minutes')
                time.sleep(120)
            if unit:
                chosenUnits[unit['name']] = {'rarity': unit['rarity'], 'gear': unit['gearTier'], 'progress': unit['gearSlotEquipped'].count(True)}
        club_data.append({'player': pd.getName(), 'id': pd.getID(), 'chosen_units': chosenUnits})

    with open(f'club_seige_progress_{datetime.datetime.now().strftime("%y%m%d")}.json', 'w') as file:
        json.dump(club_data, file)

    with open(f'club_seige_progress_{datetime.datetime.now().strftime("%y%m%d")}.csv', 'w') as file:
        csv_writer = csv.writer(file)

        #   ,       , Unit Name,     ,         , Unit Name,     ,         , ...
        # id, player,    rarity, gear, progress,    rarity, gear, progress, ...
        header1 = [None, None]
        header2 = ['id', 'player']
        for unit in CHOSEN:
            header1.append(unit.title())
            header1.extend([None, None])
            header2.extend(['rarity', 'gear', 'progress'])
        csv_writer.writerow(header1)
        csv_writer.writerow(header2)

        for player in club_data:
            row_data = [player['id'], player['player']]
            for chosen_unit in CHOSEN:
                unit_data = player['chosen_units'].get(chosen_unit.upper())
                if unit_data:
                    row_data.extend([unit_data['rarity'], unit_data['gear'], unit_data['progress']])
                else:
                    row_data.extend([None, None, None])
            csv_writer.writerow(row_data)
