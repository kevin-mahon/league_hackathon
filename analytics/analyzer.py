import json
from typing import Any
from enum import Enum, auto
import klogs
from . import analengine
from . import champions
from .stats import Statz

log = klogs.get_logger("ANALYZER")

class Analyzer:

    TRACKED_STATS = [
        ("kills", 1), #combat
        ("deaths", 1),
        ("assists", 1),
        ("totalDamageDealt", 1),
        ("magicDamageDealt", 1),
        ("physicalDamageDealt", 1),
        ("totalHeal", 1),
        ("totalDamageTaken", 1),
        ("firstBloodKill", 1),
        ("pentaKills", 1),
        ("quadraKills", 1),
        ("tripleKills", 1),
        ("doubleKills", 1),
        ("timeCCingOthers", 1),

        ("cs", 2), #economy
        ("goldEarned", 2),
        ("goldSpent", 2),

        ("visionScore", 3), #vision

        ("championId", 4), #champ select
        ("individualPosition", 4),

        ("baronKills", 5), #objectives
        ("dragonKills", 5),
        ("riftHeraldKills", 5),
        ("turretKills", 5),
        ("inhibitorKills", 5),
        ("nexusKills", 5),
        ("objectivesStolen", 5),

        ("timePlayed", 6), #general
        ("teamId", 6),
        ("role", 6),
        ("win", 6),
        # "summoner1Id", #summoner spells
        # "summoner2Id", 

    ]
    STAT_GROUPS = [
        "damage",
        "economy",
        "vision",
        "champ_select",
        "objectives",
        "general"
    ]

    # first: 
    # 1. most played champ
    # 2. time spent playing
    # 3. total kills / total deaths / total assists
    # 4. champion w/ most kills / multi kills
    # 5. total gold earned (also in lbs/ kgs)
    # 6. Monsters slain (crabs/heralds/drake/baron/atakhan)

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

        #analyze the interpreted matches
        stats = {}
        for key, category in Analyzer.TRACKED_STATS:
            stats[key] = Statz(key, 0, Category(category)) 

        for match in interpreted_matches:
            for idx, summonerId in enumerate(match.metadata.participants):
                if summonerId == puuid: #we got em boys
                    participant = match.info.participants[idx]
                    champ_id = participant.championId
                    champ_name = champions.CHAMPION_ID_TO_NAME.get(champ_id, "Unknown")
                    #update totals for overall stats
                    #loop over TRACKED_STATS and update totals by participant attributes
                    for ts in Analyzer.TRACKED_STATS:
                        #there has to be a better way to do this .. .
                        if ts == "cs":
                            stats[ts].append(participant.totalMinionsKilled + participant.neutralMinionsKilled)
                        elif ts == "championId":
                            stats[ts].append(champ_name)
                        else:
                            stats[ts].append(getattr(participant, ts))
                else:
                    continue

        #get most played champ
        most_played_champ = stats["championId"].most_common()
        most_played_champ_ngames = stats["championId"].over_time.count(most_played_champ)
        if most_played_champ:
            log.debug(f"Most played champion: {most_played_champ} with {most_played_champ_ngames} games.")

        #for all stats in totals, top_champs, most_played_champ if not in top_champs, make a result object
        individual_results = []
        for key, stat in stats.items():
            log.debug(f"Total {stat}: {stat.total}")
            individual_results.append(
                    Results(
                        name=key,
                        value=stat.total,
                        description=self.generate_description(stat, key),
                        type=stat.category
                    )
            )

        #return Results as a json serializable dict w/ individual : [total_stats]
        return [res.to_dict() for res in individual_results]
        

class Category(Enum):
    DAMAGE = 1
    ECONOMY = 2
    VISION = 3
    CHAMP_SELECT = 4
    OBJECTIVES = 5
    GENERAL = 6

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
            "category": self.type
        }

def run_analysis(summoner: str, tag: str, region: str, api_key: str = "RGAPI-342a3a00-221d-4716-a6f8-86f2e11a48aa"):
    analyzer = Analyzer(api_key)
    results = analyzer.analyze(summoner, tag, region)
    return results
