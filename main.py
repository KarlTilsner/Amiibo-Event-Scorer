from urllib.parse import urlparse
from datetime import datetime
import config
from get_tournament import tournament_ranks, multistage_tournament_ranks
from tsv import openTSV, writeTSV
from calculate_points import competitor_points, compile_points



def record_tournaments():
    # Scrapes a tournament and stores trainer ranks and tournament length
    URL = urlparse(input("Please enter a challonge URL: ")).path.strip("/")
    writeTSV(f"./Tournament Records/{URL}.tsv", tournament_ranks(URL), config.TOUR_RECORD_HEADER)

    while True:
        user_input = input("Record another tournament? [y, n]")
        if user_input == "y":
            record_tournaments()
        if user_input == "n":
            return

        print("Please enter 'y' or 'n'")



def record_multistage_tournaments():
    tours_merged = {}
    all_tours = {}
    HOST = input("Please enter the name of the tournament host: ")

    # Run a loop here to collect all tournament pools
    while True:
        user_input = input("Please enter a challonge URL or type [e] to stop recording tour pools: ") # Accepts the URL or breaks loop if e
        if user_input == "e":
            break
        URL = urlparse(user_input).path.strip("/")

        # Add info from tour to tours_merged
        tour_players, tour_details = multistage_tournament_ranks(URL, HOST)

        for player, tournament_data in tour_players.items():
            if player not in tours_merged:
                tours_merged[player] = {}

            tours_merged[player][URL] = tournament_data[URL]

        for tour, tournament_data in tour_details.items():
            if tour not in all_tours:
                all_tours[tour] = {}

            all_tours[tour] = tournament_data

    # Final check before processing
    while True:
        user_input = input("Would you like to process and save the tour pools you just collected? [y, n]")
        if user_input == "y":
            break
        if user_input == "n":
            return

        print("Please enter 'y' or 'n'")

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
        placement = data.get(FINALS_URL, f"{len(with_placement) + 1}")
        print(f"{name}: {placement}")
        final_tour_placements.append([placement, name, total_length, HOST])

    writeTSV(f"./Tournament Records/{FINALS_URL}.tsv", final_tour_placements, config.TOUR_RECORD_HEADER)
    input("Finished! Press any key to return")
    return



def main():
    config.clear_console()
    selection = input(
        "Main menu: \n"
        "(1) Record single tournaments \n"
        "(2) Record tournaments with multiple pools \n"
        "(3) Calculate trainer points from recorded tournaments \n"
        "(4) Calculate host points from recorded tournaments \n"
        "(E) Exit \n"
        )

    match selection:
        case "1":
            record_tournaments()
        case "2":
            record_multistage_tournaments()
        case "3":
            compile_points()
        case "4":
            input("WIP, press any key to return")
        case "e":
            return
        case _:
            print(f"Invalid selection: {selection} (must be one of the above)")
            print("\n \n \n")
            main()

    main()



if __name__ == "__main__":
    main()