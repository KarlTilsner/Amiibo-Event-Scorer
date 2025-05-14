import challonge
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



def multistage_tournament_ranks(URL, HOST):
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



def tournament_length(URL):
    matches = challonge.matches.index(URL)
    tour_length = len(matches)
    return tour_length
