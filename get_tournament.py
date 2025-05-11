import challonge
import config

challonge.set_credentials(config.CHALLONGE_USERNAME, config.CHALLONGE_API_KEY)



def tournament_ranks(URL):
    participants = challonge.participants.index(URL)
    participants_sorted = sorted(participants, key=lambda p: p["final_rank"] or float("inf"))
    tour_len = tournament_length(URL)

    recorded_data = []
    for p in participants_sorted:
        recorded_data.append([p["final_rank"], p["display_name"], tour_len])

    return recorded_data



def tournament_length(URL):
    matches = challonge.matches.index(URL)
    tour_length = len(matches)
    print(tour_length)
    return tour_length
