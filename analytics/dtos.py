import json
from typing import Any, Dict, get_args, get_origin
from dataclasses import dataclass, fields, asdict, is_dataclass

BLACLIST = ['perks', 'missions', 'challenges']

@dataclass
class BaseDTO:
    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        init_data = {}
        for f in fields(cls):
            value = data.get(f.name)

            ftype = f.type
            origin = get_origin(ftype)

            # Case 1: direct dataclass
            if is_dataclass(ftype) and isinstance(value, dict):
                init_data[f.name] = ftype.from_dict(value)

            # Case 2: list of dataclasses
            elif origin in (list, tuple):
                (elem_type,) = get_args(ftype) or (None,)
                if elem_type and is_dataclass(elem_type) and isinstance(value, list):
                    init_data[f.name] = [elem_type.from_dict(v) if isinstance(v, dict) else v
                                         for v in value]
                else:
                    init_data[f.name] = value           
            else:
                init_data[f.name] = value
        return cls(**init_data)

    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))

@dataclass
class ParticipantDTO(BaseDTO):
    assists: int
    baronKills: int
    bountyLevel: int
    champExperience: int
    champLevel: int
    championId: int
    championName: str
    championTransform: int
    consumablesPurchased: int
    damageDealtToBuildings: int
    damageDealtToObjectives: int
    damageDealtToTurrets: int
    damageSelfMitigated: int
    deaths: int
    detectorWardsPlaced: int
    doubleKills: int
    dragonKills: int
    firstBloodAssist: bool
    firstBloodKill: bool
    firstTowerAssist: bool
    firstTowerKill: bool
    gameEndedInEarlySurrender: bool
    gameEndedInSurrender: bool
    goldEarned: int
    goldSpent: int
    individualPosition: str
    inhibitorKills: int
    inhibitorTakedowns: int
    inhibitorsLost: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    itemsPurchased: int
    killingSprees: int
    kills: int
    lane: str
    largestCriticalStrike: int
    largestKillingSpree: int
    largestMultiKill: int
    longestTimeSpentLiving: int
    magicDamageDealt: int
    magicDamageDealtToChampions: int
    magicDamageTaken: int
    neutralMinionsKilled: int
    nexusKills: int
    nexusLost: int
    nexusTakedowns: int
    objectivesStolen: int
    objectivesStolenAssists: int
    participantId: int
    pentaKills: int
    perks : dict
    physicalDamageDealt : int
    physicalDamageDealtToChampions : int
    physicalDamageTaken : int
    profileIcon : int
    puuid : str
    quadraKills :int 
    riotIdName : str
    riotIdTagline : str
    role : str
    sightWardsBoughtInGame :int 
    spell1Casts :int 
    spell2Casts :int 
    spell3Casts :int 
    spell4Casts :int 
    summoner1Casts :int
    summoner1Id :int
    summoner2Casts :int
    summoner2Id :int
    summonerId :str
    summonerLevel :int
    summonerName :str
    teamEarlySurrendered :bool
    teamId :int
    teamPosition :str
    timeCCingOthers :int
    timePlayed :int
    totalAllyJungleMinionsKilled : int 
    totalDamageDealt : int 
    totalDamageDealtToChampions :int 
    totalDamageShieldedOnTeammates :int 
    totalDamageTake :int 
    totalEnemyJungleMinionsKilled :int 
    totalHeal :int 
    totalHealsOnTeammates :int
    totalMinionsKilled : int
    totalTimeCCDealt:int 
    totalTimeSpentDead :int 
    totalUnitsHealed:int 
    tripleKills:int 
    trueDamageDealt :int 
    trueDamageDealtToChampions :int 
    trueDamageTaken:int 
    turretKills :int 
    turretTakedowns :int 
    turretsLost :int 
    unrealKills :int 
    visionScore :int 
    visionClearedPings :int 
    visionWardsBoughtInGame :int 
    wardsKilled :int 
    wardsPlaced :int 
    win : bool 

@dataclass
class BanDTO(BaseDTO):
    championId: int
    pickTurn: int

@dataclass
class ObjectiveDTO(BaseDTO):
    first: bool
    kills: int

@dataclass
class ObjectivesDTO(BaseDTO):
    baron: ObjectiveDTO
    champion: ObjectiveDTO
    dragon: ObjectiveDTO
    horde: ObjectiveDTO
    inhibitor: ObjectiveDTO
    riftHerald: ObjectiveDTO
    tower: ObjectiveDTO

class TeamDTO(BaseDTO):
    bans: list[BanDTO]
    objectives: ObjectivesDTO
    teamId: int
    win : bool

@dataclass
class InfoDTO(BaseDTO):
    endOfGameResult : str
    gameCreation : int
    gameDuration : int
    gameEndTimestamp : int
    gameId : int
    gameMode : str
    gameName: int
    gameType : str
    gameVersion : str
    mapId : int
    participants : list[ParticipantDTO]
    platformId : str
    queueId : int
    teams : list[TeamDTO]
    tournamentCode : str

@dataclass
class MetadataDTO(BaseDTO):
    dataVersion : str
    matchId : str
    participants : list[str]

@dataclass
class MatchDTO(BaseDTO):
    metadata : MetadataDTO
    info : InfoDTO

