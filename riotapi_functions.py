import time
import json
from requests_html import HTMLSession


def get_puuid(puuid_url, api_key, user):
    """Return the puuid of a player given its gametag and tagline
       -PUUID_URL is a string containing the api url
       -USER is a list containing gametag and tigline strings
    """
    session = HTMLSession()
    response = session.get(puuid_url+user[0]+'/'+user[1],
                           headers={"X-Riot-Token": api_key})
    if response.status_code == 200:
        return json.loads(response.text)['puuid']
    else:
        return f"{response.status_code}"


def get_matchlist(matchslist_url, api_key, puuid, end):
    """return the last 100 matches between start and end epoch given a puuid"""
    time.sleep(2)
    session = HTMLSession()
    response = session.get(f"{matchslist_url}{puuid}/ids?endTime={end}&start=0&count=50",
                           headers={"X-Riot-Token": api_key})
    return json.loads(response.text)


def get_matchdata(matchdata_url, api_key, matchid):
    """return the match data given a match_id"""
    time.sleep(1.5)
    session = HTMLSession()
    response = session.get(f"{matchdata_url}{matchid}",
                           headers={"X-Riot-Token": api_key})
    return json.loads(response.text)
