from urllib.parse import urlparse
import config
from get_tournament import tournament_ranks, tournament_length
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
            main()

        print("Please enter 'y' or 'n'")



def main():
    config.clear_console()
    selection = input(
        "Main menu: \n"
        "(1) Record challonge tournaments \n"
        "(2) Calculate trainer points from recorded tournaments \n"
        "(3) Calculate host points from recorded tournaments \n"
        "(E) Exit \n"
        )

    match selection:
        case "1":
            record_tournaments()
        case "2":
            compile_points()
        case "3":
            input("WIP, press any key to return")
        case "e":
            return
        case _:
            print(f"Invalid selection: {selection} (must be 1, 2, 3)")
            print("\n \n \n")
            main()

    main()



if __name__ == "__main__":
    main()