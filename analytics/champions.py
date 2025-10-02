#convert champion ID to champion name
import json
import os
import pickle

with open(os.path.join(os.path.dirname(__file__), "champions.pkl"), "rb") as f:
    champs = pickle.load(f)

CHAMPION_ID_TO_NAME = {}
for k, v in champs.items():
    CHAMPION_ID_TO_NAME[int(v['key'])] = v['name']