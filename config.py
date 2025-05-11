import json

with open("config.json", "r") as file:
    config = json.load(file)

CHALLONGE_USERNAME = config["challonge_username"]
CHALLONGE_API_KEY = config["challonge_api_key"]

TOUR_RECORD_HEADER = ["Rank", "Trainer", "Tournament Length"]
COMPETITOR_POINTS_HEADER = ["Rank", "Trainer", "Points"]