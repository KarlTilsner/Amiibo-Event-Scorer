import json
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

with open("api_key.json", "r") as file:
    api = json.load(file)

CHALLONGE_USERNAME = api["challonge_username"]
CHALLONGE_API_KEY = api["challonge_api_key"]

with open("base_points.json", "r") as file:
    base_points = json.load(file)


TOUR_RECORD_HEADER = ["Rank", "Trainer", "Tournament Length"]
COMPETITOR_POINTS_HEADER = ["Rank", "Trainer", "Points"]