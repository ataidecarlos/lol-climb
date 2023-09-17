import constants
import requests, json
from dataclasses import dataclass

@dataclass
class Summoner:
    name: str
    summoner_id: str
    tier: str
    league_points: int
    wins: int
    losses: int


APIKEY: str = constants.RIOT_API

def get_summoner_id(summoner: str) -> str:
    """Returns the summoners id, taking summoner name as input."""
    uri: str = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={APIKEY}'

    result  = requests.get(uri)
    if (result.status_code != 200):
        return (result.status_code) * -1
    
    return json.loads(result.content)['id']


def get_summoner_details(summoner_id: int) -> Summoner:
    """Returns Summoner dataclass, takes summoner id as input."""
    
    # This API call returns a list with details for every queue type (RANKED_SOLO_5x5, RANKED_FLEX_SR, etc)
    uri = f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={APIKEY}'
    
    result = requests.get(uri)
    if (result.status_code != 200):
        return (result.status_code) * -1
    
    current_summoner: Summoner = filter_result(json.loads(result.content))
    return current_summoner


def filter_result(summoner_json) -> Summoner:
    """Grab only relevant data from JSON response"""
    for current_q in summoner_json:
        if current_q['queueType'] == "RANKED_SOLO_5x5":

            summoner = Summoner(
                current_q['summonerName'],
                current_q['summonerId'],
                current_q['tier'],
                current_q['leaguePoints'],
                current_q['wins'],
                current_q['losses']
            )

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
    summoner_id = get_summoner_id('thebausffs')
    if type(summoner_id) == int:
        print(summoner_id)
        quit()
    
    thebausffs: Summoner = get_summoner_details(summoner_id)
    print(f'Tier: {thebausffs.tier}, Points: {thebausffs.league_points}')