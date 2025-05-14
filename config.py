import json
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

with open("config.json", "r") as file:
    config = json.load(file)

CHALLONGE_USERNAME = config["challonge_username"]
CHALLONGE_API_KEY = config["challonge_api_key"]
COMPETITOR_BASE_POINTS = config["competitor_base_points"]
TOUR_RECORD_HEADER = config["tour_record_header"]
COMPETITOR_POINTS_HEADER = config["competitor_points_header"]
COMPETITOR_BONUS_POINTS = config["competitor_bonus_points"]