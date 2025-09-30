import requests
import time
import klogs
import pandas as pd
from . import dtos
from datetime import datetime, timedelta

log = klogs.get_logger("ANALYTICS")


REGION_MAP = {
    "na1": "americas",
    "br1": "americas",
    "la1": "americas",
    "la2": "americas",
    "euw1": "europe",
    "eun1": "europe",
    "tr1": "europe",
    "ru": "europe",
    "kr": "asia",
    "jp1": "asia",
    "oc1": "sea",
    "ph2": "sea",
    "sg2": "sea",
    "th2": "sea",
    "tw2": "sea",
    "vn2": "sea",
}

class Analytics:

    def __init__(self, riot_api_key: str):
        self.api_key = riot_api_key

    def get_summoner_puuid(self, summoner_name: str, tag : str, region: str) -> str:
        """Get the PUUID for a given summoner name."""
        log.debug(f"Fetching PUUID for summoner: {summoner_name}#{tag} in region: {region}")
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}"#summoner/v4/summoners/by-name/{summoner_name}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["puuid"]

    def get_matches_last_year(self, summoner_name: str, tag : str, platform: str, count: int = 100, stop_condition  = None) -> list[str]:
        """Get all match IDs from the past year for a summoner."""
        region = REGION_MAP[platform]
        puuid = self.get_summoner_puuid(summoner_name, tag, region)
        log.debug(f"Summoner PUUID: {puuid}")

        # Calculate time range
        end_time = int(time.time())  # now 
        start_time = int((datetime.now() - timedelta(days=365)).timestamp())

        all_matches = []
        start = 0
        while True:
            url = (
                f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/"
                f"{puuid}/ids?start={start}&count={count}&startTime={start_time}&endTime={end_time}"
            )
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            matches = response.json()

            if not matches:
                break

            all_matches.extend(matches)
            start += count

            if stop_condition and len(all_matches) >= stop_condition:
                log.warning(f"Stop condition of {stop_condition} matches reached.")
                break

        log.debug(f"Total matches fetched: {len(all_matches)}")
        log.debug(f"First 5 matches: {all_matches[:5]}")
        return all_matches

    def get_match_details(self, match_id: str, platform: str) -> str:
        """Get detailed match information for a given match ID."""
        region = REGION_MAP[platform]
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def interpret_match(self, match_data: str) -> dtos.MatchDTO:
        """Interpret raw match data into structured DTOs."""
        match_dto = dtos.MatchDTO.from_json(match_data)
        return match_dto

    def get_champion_mastery(self, summoner_name: str, tag : str, platform: str) -> list[dict]:
        """Get champion mastery data for a given summoner."""
        region = REGION_MAP[platform]
        puuid = self.get_summoner_puuid(summoner_name, tag, region)
        log.debug(f"Fetching champion mastery for PUUID: {puuid}")
        url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{puuid}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_league_entries(self, summoner_name: str, tag : str, platform: str) -> list[dict]:
        """Get league entries for a given summoner."""
        region = REGION_MAP[platform]
        puuid = self.get_summoner_puuid(summoner_name, tag, region)
        log.debug(f"Fetching league entries for PUUID: {puuid}")
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{puuid}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

def run_analysis(summoner: str, tag: str, platform: str, riot_api_key: str):
    analytics = Analytics(riot_api_key)

    detailed_match_list = []
    matches = analytics.get_matches_last_year(summoner, tag, platform, stop_condition=10)
    for match in matches[0:2]:
        detailed_match = analytics.get_match_details(match, platform)
        detailed_match_list.append(analytics.interpret_match(detailed_match))

    #save detailed_match_list object to a pkl file
    import pickle
    with open("detailed_matches.pkl", "wb") as f:
        pickle.dump(detailed_match_list, f)

    df = pd.DataFrame([match.to_dict() for match in detailed_match_list])
    df.to_csv("detailed_matches.csv", index=False)

