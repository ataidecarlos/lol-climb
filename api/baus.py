import requests
import json
from dataclasses import dataclass

@dataclass
class Summoner:
    name: str
    summoner_id: str
    tier: str
    league_points: int
    wins: int
    losses: int


APIKEY: str = 'RGAPI-4b675324-2d89-4a01-8d45-3a9b770592b6'

def fetch_from_api(summoner: str):
    # get the summoner by id
    uri: str = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={APIKEY}'
    
    result  = requests.get(uri)
    if (result.status_code != 200):
        return (result.status_code + 1000) * -1
    
    # get summoner details
    summoner_id = json.loads(result.content)['id']
    uri = f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={APIKEY}'
    
    result  = requests.get(uri)
    if (result.status_code != 200):
        return (result.status_code + 2000) * -1
    
    result_json = json.loads(result.content) # this will return a list, each element is type of queue in the game
    return result_json


def summoner_details(result_json):
    for current_q in result_json:
        if current_q['queueType'] == "RANKED_SOLO_5x5":

            summoner = Summoner(
                current_q['summonerName'],
                current_q['summonerId'],
                current_q['tier'],
                current_q['leaguePoints'],
                current_q['wins'],
                current_q['losses']
            )

            #pprint(summoner)
            return(summoner)

        else:
            continue
    ...


def placement(summoner: Summoner):

    message: str = "Long way to go ..."

    if summoner.tier == "CHALLENGER":
        message = f'Tier: {summoner.tier}, points: 123'
    elif summoner.tier == "GRANDMASTER":
        message = f'Tier: {summoner.tier}. Getting close.'
    elif summoner.tier == "MASTER":
        message = f'Tier: {summoner.tier}. The climb is real!'

    print(message)
    #nothing
    ...

    


if __name__ == "__main__":
    result = fetch_from_api('thebausffs')
    if type(result) == int:
        print(result)
        quit()
    
    summoner = summoner_details(result)
    placement(summoner)