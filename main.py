from datetime import datetime
import pandas as pd
from pymongo import MongoClient
from riotapi_functions import *

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 20)

API_KEY = 'RGAPI-1497b4c3-048f-4d37-b2f6-c397facefde7'
PUUID_URL = 'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'
MATCHSLIST_URL = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
MATCHDATA_URL = "https://europe.api.riotgames.com/lol/match/v5/matches/"

USERS = [{"gameName": "", "tagLine": ""}]
PLAYER = "Colossal Enculé".replace(' ', '%20')
show_firstgames = True

client = MongoClient('localhost', 27017)
db = client.TSL
players = db.players
games = db.games

# ADD PLAYERS #

if USERS[0]["gameName"] != "":
    for i, user in enumerate(USERS):
        user_pair = [user["gameName"], user["tagLine"]]
        USERS[i]["puuid"] = get_puuid(PUUID_URL, API_KEY, user_pair)

    players.update_many(USERS)


# ADD GAMES #

if PLAYER != '':
    puuid = players.find_one({"gameName": PLAYER})["puuid"]
    try:
        first_game = games.find({"metadata.participants": puuid},
                                {'info.gameCreation': 1, '_id': 0}).sort('info.gameCreation',
                                                                         1).limit(1)[0]["info"]["gameCreation"]
    except:
        print('adding games from today')
        first_game = int(datetime.now().timestamp())

    matchList = get_matchlist(MATCHSLIST_URL, API_KEY, puuid, int(first_game/1000))
    if len(matchList) == 0:
        print('no games found')
    matchs = []
    for m in matchList:
        print(m)
        matchdata = get_matchdata(MATCHDATA_URL, API_KEY, m)
        games.update_one({'metadata.matchId': matchdata['metadata']['matchId']}, {"$set": matchdata}, upsert=True)


if show_firstgames:
    players_list = players.find()
    for p in players_list:
        first_game = games.find(
            {"metadata.participants": p['puuid']},
            {'info.gameCreation': 1, '_id': 0}).sort('info.gameCreation',
                                                     1).limit(1)[0]["info"]["gameCreation"]
        print(p['gameName'].replace('%20', ' '), datetime.fromtimestamp(int(first_game/1000)))
