from urllib.parse import urlparse
import config
from tsv import openTSV, writeTSV, getAllInFolder
import get_tournament
import calculate_points



def record_tournaments():
    # Scrapes a tournament and stores trainer ranks and tournament length
    URL = urlparse(input("Please enter a challonge URL: ")).path.strip("/")
    writeTSV(f"./Tournament Records/{URL}.tsv", get_tournament.tournament_ranks(URL), config.TOUR_RECORD_HEADER)

    while True:
        user_input = input("Record another tournament? [y, n]: ")
        if user_input == "y":
            print("\n")
            record_tournaments()
        if user_input == "n":
            return

        print("Please enter 'y' or 'n'")



def record_multistage_tournaments():
    HOST = input("Please enter the name of the tournament host: ")

    # Loops untll user has entered all pools
    tours_merged, all_tours = get_tournament.get_bracket_pools()

    # Final check before processing
    while True:
        user_input = input("Would you like to process and save the tour pools you just collected? [y, n]: ")
        if user_input == "y":
            break
        if user_input == "n":
            return

        print("Please enter 'y' or 'n'")

    final_tour_placements, FINALS_URL = get_tournament.determine_multistage_ranks(tours_merged, all_tours, HOST)

    writeTSV(f"./Tournament Records/{FINALS_URL}.tsv", final_tour_placements, config.TOUR_RECORD_HEADER)
    input("Finished! Press any key to return")
    return



def compile_competitor_points():
    filepaths = getAllInFolder()
    total_points = {}

    for path in filepaths:
        # Returns a dictionary of trainers and their scores from passed tournament
        tour_points = calculate_points.competitor_points(openTSV(path))

        for trainer, points in tour_points.items():
            total_points[f"{trainer}"] = total_points.get(f"{trainer}", 0) + points

    total_points = dict(sorted(total_points.items(), key=lambda item: item[1], reverse=True))

    tsv_data = []
    for i, (trainer, points) in enumerate(total_points.items(), start=1):
        tsv_data.append([i, trainer, points])
    
    writeTSV("./Spreadsheets/Competitor Points.tsv", tsv_data, config.COMPETITOR_POINTS_HEADER)

    input("Finished! Press any key to return to the menu.")
    return



def compile_host_points():
    filepaths = getAllInFolder()
    total_points = {}

    for path in filepaths:
        # Returns a dictionary of hosts and their scores from passed tournament
        tour_points, host_name = calculate_points.host_points(openTSV(path))

        total_points[f"{host_name}"] = total_points.get(f"{host_name}", 0) + tour_points
         
        
    total_points = dict(sorted(total_points.items(), key=lambda item: item[1], reverse=True))

    tsv_data = []
    for i, (host, points) in enumerate(total_points.items(), start=1):
        tsv_data.append([i, host, points])
    
    writeTSV("./Spreadsheets/Host Points.tsv", tsv_data, config.HOST_POINTS_HEADER)

    input("Finished! Press any key to return to the menu.")
    return



def main():
    config.clear_console()
    selection = input(
        "Main menu: \n"
        "(1) Record single tournaments \n"
        "(2) Record tournaments with multiple pools \n"
        "(3) Calculate competitor points from recorded tournaments \n"
        "(4) Calculate host points from recorded tournaments \n"
        "(E) Exit \n"
        )

    match selection:
        case "1":
            record_tournaments()
        case "2":
            record_multistage_tournaments()
        case "3":
            compile_competitor_points()
        case "4":
            compile_host_points()
        case "e":
            return
        case _:
            print(f"Invalid selection: {selection} (must be one of the above)")
            print("\n \n \n")
            main()

    main()



if __name__ == "__main__":
    main()