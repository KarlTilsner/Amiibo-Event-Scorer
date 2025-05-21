import challonge
from urllib.parse import urlparse
from datetime import datetime
import config

challonge.set_credentials(config.CHALLONGE_USERNAME, config.CHALLONGE_API_KEY)



def tournament_ranks(URL):
    HOST = input("Please enter the name of the tournament host: ")
    participants = challonge.participants.index(URL)
    participants_sorted = sorted(participants, key=lambda p: p["final_rank"] or float("inf"))
    tour_len = tournament_length(URL)

    recorded_data = []
    for p in participants_sorted:
        recorded_data.append([p["final_rank"], p["display_name"], tour_len, HOST])

    return recorded_data



def multistage_tournament_ranks(URL):
    participants = challonge.participants.index(URL)
    tournament = challonge.tournaments.show(URL)

    end_time = tournament["completed_at"]

    participants_sorted = sorted(participants, key=lambda p: p["final_rank"] or float("inf"))
    tour_len = tournament_length(URL)

    recorded_data = {}
    tour_details = {URL: {"tour_length": tour_len, "completed_at": f"{end_time}"}}
    for p in participants_sorted:
        recorded_data[f'{p["display_name"]}'] = {URL: p["final_rank"]}

    return recorded_data, tour_details



def get_bracket_pools():
    tours_merged = {}
    all_tours = {}

    # Run a loop here to collect all tournament pools
    while True:
        user_input = input("Please enter a challonge URL or type [e] to stop recording tour pools: ") # Accepts the URL or breaks loop if e
        if user_input == "e":
            break
        URL = urlparse(user_input).path.strip("/")

        # Add info from tour to tours_merged
        tour_players, tour_details = multistage_tournament_ranks(URL)

        for player, tournament_data in tour_players.items():
            if player not in tours_merged:
                tours_merged[player] = {}

            tours_merged[player][URL] = tournament_data[URL]

        for tour, tournament_data in tour_details.items():
            if tour not in all_tours:
                all_tours[tour] = {}

            all_tours[tour] = tournament_data
    
    return tours_merged, all_tours



def determine_multistage_ranks(tours_merged, all_tours, HOST):
    # Filter out items where 'completed_at' is the string "None"
    valid_tours = [
        (name, data)
        for name, data in all_tours.items()
        if data.get("completed_at") != "None"
    ]

    # Only proceed if we have at least one valid entry
    if valid_tours:
        latest_tour = max(
            valid_tours,
            key=lambda item: datetime.fromisoformat(item[1]["completed_at"])
        )
        print("Latest tournament:", latest_tour[0])
    else:
        print("No tournaments with valid completed_at date.")

    tours_merged = dict(sorted(
        tours_merged.items(),
        key=lambda item: len(item[1]),
        reverse=True
    ))

    FINALS_URL = latest_tour[0]
    with_placement = []
    without_placement = []

    for name, data in tours_merged.items():
        if FINALS_URL in data:
            with_placement.append((name, data))
        else:
            without_placement.append((name, data))

    # Sort only the ones with placements
    with_placement.sort(key=lambda x: x[1][FINALS_URL])

    # Combine the two lists
    sorted_all = with_placement + without_placement

    total_length = sum(tour["tour_length"] for tour in all_tours.values())

    # After collecting tournament pool info
    final_tour_placements = []
    # Print them
    for name, data in sorted_all:
        if len(with_placement) < 32:
            placement = data.get(FINALS_URL, f"{33}")

        if len(with_placement) >= 32:
            placement = data.get(FINALS_URL, f"{len(with_placement) + 1}")

        # print(f"{name}: {placement}")
        final_tour_placements.append([placement, name, total_length, HOST])

    return final_tour_placements, FINALS_URL



def tournament_length(URL):
    matches = challonge.matches.index(URL)
    tour_length = len(matches)
    return tour_length
