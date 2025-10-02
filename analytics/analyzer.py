import json
import klogs
from . import analengine
from . import champions

log = klogs.get_logger("ANALYZER")

class Analyzer:

    def __init__(self, riot_api_key: str):
        self.engine = analengine.Analytics(riot_api_key)

    def analyze(self, summoner: str, tag : str, region : str):
        #what do we need? 
        # 1. we need the summoner name and tag & region
        # 2. we need to get the puuid
        # 3. we need to get the last year of match history
        # 4. we need to get the match details for each match
        # 5. we need to interpret the match details into DTOs
        # 6. we need to get the champion mastery for top 3 champions
        # 7. using the interpreted match details we need to:
        #   a. get the total number of games played
        #   b. get the win rate for each champion
        #   ci. get the average KDA
        #   cii. get total kills deaths assists
        #   d. get the average CS
        #   e. get the average gold
        #   f. get the average damage 
        #   g. get the average vision score

        #1 & 2
        puuid = self.engine.get_summoner_puuid(summoner, tag, region)
        #3
        matches = self.engine.get_matches_last_year(puuid, region)
        #4
        detailed_matches = []
        for match in matches:
            detailed_match = self.engine.get_match_details(match, region)
            detailed_matches.append(detailed_match)
        #5
        interpreted_matches = []
        for detailed_match in detailed_matches:
            interpreted_match = self.engine.interpret_match(detailed_match)
            interpreted_matches.append(interpreted_match)
        #6
        #get champion mastery for top 3 champions
        champion_mastery = self.engine.get_champion_mastery(puuid, region)
        champion_mastery_dtos = []
        for cm in json.loads(champion_mastery):
            champion_mastery_dtos.append(self.engine.interpret_champ_mastery(cm))
        #7
        #analyze the interpreted matches
        total_games = len(interpreted_matches)
        champion_stats = {}
        total_kills = 0
        total_deaths = 0
        total_assists = 0
        total_cs = 0
        total_gold = 0
        total_damage = 0
        total_vision = 0
        for match in interpreted_matches:
            for idx, summonerId in enumerate(match.metadata.participants):
                if summonerId == puuid:
                    participant = match.info.participants[idx]
                    champ_id = participant.championId
                    champ_name = champions.CHAMPION_ID_TO_NAME.get(champ_id, "Unknown")
                    if champ_name not in champion_stats:
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

                    total_kills += participant.kills
                    total_deaths += participant.deaths
                    total_assists += participant.assists
                    total_cs += participant.totalMinionsKilled + participant.neutralMinionsKilled
                    total_gold += participant.goldEarned
                    total_damage += participant.totalDamageDealtToChampions
                    total_vision += participant.visionScore
        
        #top champ masteries:
        top_champs = []
        for cm in champion_mastery_dtos:
            top_champs.append(champions.CHAMPION_ID_TO_NAME.get(cm.championId, "Unknown"))
        log.debug(f"Top champions by mastery: {top_champs}")
        top_champ_stats = {champ: champion_stats.get(champ, {}) for champ in top_champs}
        #now return the analysis in JSON format, i.e. as a dict
        return {
            "total_games": total_games,
            "total_kills": total_kills,
            "total_deaths": total_deaths,
            "total_assists": total_assists,
            "total_cs": total_cs,
            "total_gold": total_gold,
            "total_damage": total_damage,
            "total_vision": total_vision,
            "average_kda": {
                "kills": total_kills / total_games if total_games > 0 else 0,
                "deaths": total_deaths / total_games if total_games > 0 else 0,
                "assists": total_assists / total_games if total_games > 0 else 0
            },
            "average_cs": total_cs / total_games if total_games > 0 else 0,
            "average_gold": total_gold / total_games if total_games > 0 else 0,
            "average_damage": total_damage / total_games if total_games > 0 else 0,
            "average_vision": total_vision / total_games if total_games > 0 else 0,
            "champion_stats": top_champ_stats,
            "top_champions": top_champs  # top 3 champions by mastery
        }