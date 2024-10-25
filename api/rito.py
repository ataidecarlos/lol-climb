import constants
import requests, json
from dataclasses import dataclass

# Rewriting the whole thing as the latest API version forces the usage of Riot ID and is not backwards compatible

@dataclass
class summoner:
    id: str
    accountId: str
    puuid: str
    profileIconId: int
    revisionDate: int
    summonerLevel: int
    gameName: str
    tagLine: str

APIKEY: str = constants.RIOT_API

def control_by_puuid(current: summoner, region: str) -> str:
    """Returns Summoner dataclass, takes ign and tagLine as input."""
    uri: str = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{current.puuid}?api_key={APIKEY}'

    result  = requests.get(uri)
    if (result.status_code != 200):
        return (result.status_code) * -1
    
    current.puuid = json.loads(result.content)['puuid']
    current.gameName = json.loads(result.content)['gameName']
    current.tagLine = json.loads(result.content)['tagLine']
    return current

def get_summoner_details(current: summoner, server) -> summoner:
    """Returns summoner dataclass, takes puuid as input."""
    
    uri = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{current.puuid}?api_key={APIKEY}'
    
    result = requests.get(uri)
    if (result.status_code != 200):
        return (result.status_code) * -1
    
    current.profileIconId = json.loads(result.content)['profileIconId']
    current.revisionDate = json.loads(result.content)['revisionDate']
    current.summonerLevel = json.loads(result.content)['summonerLevel']
    return current


if __name__ == "__main__":
    
    # This is hardcorded, both as an example on how to get started in collecting the rest of the data, as well as a control
    # puuid = cwMcGIF_5yzQF-un6ytkmvpbfSyK_sdbckJWKgXmPBjxqJqQs1xcGMdwTenUFMxcec0jTJHqOkqBTA

    region: str = "europe"
    server: str = "euw1"

    thebausffs = summoner(
        id="0wHjHMzY2DfBScnTL5rkgeA5Vv-VpcXI0vzEr88Py_x-boTr",
        accountId="xc-weeq93oZB_S1U1hOhevG8EWr1HIZ6NKiZqWPAzSkagBU",
        puuid="cwMcGIF_5yzQF-un6ytkmvpbfSyK_sdbckJWKgXmPBjxqJqQs1xcGMdwTenUFMxcec0jTJHqOkqBTA",
        profileIconId=0,
        revisionDate=0,
        summonerLevel=0,
        gameName="",
        tagLine=""
    )
    print(thebausffs)

    control: summoner = control_by_puuid(thebausffs, region)    
    if control.puuid != thebausffs.puuid:
        print(f"Error: puuid mismatch. {control.puuid} != {thebausffs.puuid}")
        quit()
    
    thebausffs.gameName = control.gameName
    thebausffs.tagLine = control.tagLine
    print(thebausffs)

    thebausffs = get_summoner_details(thebausffs, server)
    print(thebausffs)
    


