import json
from typing import Any
from enum import Enum, auto
import klogs
from . import analengine
from . import champions

log = klogs.get_logger("ANALYZER")

class Analyzer:

    TRACKED_STATS = [
        "kills",
        "deaths",
        "assists",
        "cs",
        "goldEarned",
        "totalDamageDealtToChampions",
        "visionScore"
    ]
    STAT_GROUPS = [
        "damage",
        "economy",
        "vision",
        "champ_select",
    ]

    def __init__(self, riot_api_key: str):
        self.engine = analengine.Analytics(riot_api_key)

    def generate_description(self, stat: str, value: Any) -> str:
        #PLACEHOLDER
        return f"You had a total of {value} {stat} in the last year!"

    def analyze(self, summoner: str, tag : str, region : str):
        puuid = self.engine.get_summoner_puuid(summoner, tag, region)
        if not puuid:
            log.error(f"Could not find puuid for summoner {summoner} in region {region}")
            return None
        matches = self.engine.get_matches_last_year(puuid, region)

        #get detailed match info for each match
        detailed_matches = []
        for match in matches:
            detailed_match = self.engine.get_match_details(match, region)
            detailed_matches.append(detailed_match)

        #interpret the matches
        interpreted_matches = []
        for detailed_match in detailed_matches:
            interpreted_match = self.engine.interpret_match(detailed_match)
            interpreted_matches.append(interpreted_match)

        #get champion mastery for top 3 champions
        champion_mastery = self.engine.get_champion_mastery(puuid, region)
        champion_mastery_dtos = []
        for cm in json.loads(champion_mastery):
            champion_mastery_dtos.append(self.engine.interpret_champ_mastery(cm))

        #analyze the interpreted matches
        total_games = len(interpreted_matches)
        champion_stats = {}

        totals = {}
        for key in Analyzer.TRACKED_STATS:
            totals[key] = 0

        for match in interpreted_matches:
            for idx, summonerId in enumerate(match.metadata.participants):
                if summonerId == puuid:
                    participant = match.info.participants[idx]
                    champ_id = participant.championId
                    champ_name = champions.CHAMPION_ID_TO_NAME.get(champ_id, "Unknown")

                    if champ_name not in champion_stats:
                        #this is ugly and I hate it
                        champion_stats[champ_name] = {
                            "games": 0,
                            "wins": 0,
                            "kills": 0,
                            "deaths": 0,
                            "assists": 0,
                            "cs": 0,
                            "gold": 0,
                            "damage": 0,
                            "vision": 0
                        }

                    champion_stats[champ_name]["games"] += 1
                    if participant.win:
                        champion_stats[champ_name]["wins"] += 1

                    champion_stats[champ_name]["kills"] += participant.kills
                    champion_stats[champ_name]["deaths"] += participant.deaths
                    champion_stats[champ_name]["assists"] += participant.assists
                    champion_stats[champ_name]["cs"] += participant.totalMinionsKilled + participant.neutralMinionsKilled
                    champion_stats[champ_name]["gold"] += participant.goldEarned
                    champion_stats[champ_name]["damage"] += participant.totalDamageDealtToChampions
                    champion_stats[champ_name]["vision"] += participant.visionScore

                    #update totals for overall stats
                    #loop over TRACED_STATS and update totals by participant attributes
                    for stat in Analyzer.TRACKED_STATS:
                        totals[stat] += getattr(participant, stat) if stat != "cs" else (participant.totalMinionsKilled + participant.neutralMinionsKilled)

        #top champ masteries:
        top_champs = []
        for cm in champion_mastery_dtos:
            top_champs.append(champions.CHAMPION_ID_TO_NAME.get(cm.championId, "Unknown"))

        log.debug(f"Top champions by mastery: {top_champs}")
        top_champ_stats = {champ: champion_stats.get(champ, {}) for champ in top_champs}

        #get most played champ
        most_played_champ = max(champion_stats.items(), key=lambda x: x[1]["games"], default=(None, None))
        if most_played_champ[0]:
            log.debug(f"Most played champion: {most_played_champ[0]} games")

        #for all stats in totals, top_champs, most_played_champ if not in top_champs, make a result object
        individual_results = []
        for stat, value in totals.items():
            log.debug(f"Total {stat}: {value}")
            individual_results.append(
                    Results(
                        name=stat,
                        value=value,
                        description=self.generate_description(stat, value),
                        type=Category.SOLO
                    )
            )

        #return Results as a json serializable dict w/ individual : [total_stats]
        return {
            "individual": [res.to_dict() for res in individual_results],
            "groups": []
        }

class Category(Enum):
    SOLO = 1
    GROUP = 2
    WRAPPED = 3

class Results:
    name: str
    value : Any
    description : str
    type: Category 

    def __init__(self, name: str, value: Any, description: str, type: Category):
        self.name = name
        self.value = value
        self.description = description
        self.type = type

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "description": self.description,
            "type": self.type
        }
