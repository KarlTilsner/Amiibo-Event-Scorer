from urllib.parse import urlparse
import config
from get_tournament import tournament_ranks, tournament_length
from tsv import openTSV, writeTSV
from calculate_points import competitor_points



def main():
    # Scrapes a tournament and stores trainer ranks and tournament length
    URL = urlparse(input("Please enter a challonge URL: ")).path.strip("/")
    trainer_ranks = tournament_ranks(URL)
    writeTSV(f"./Tournament Records/{URL}.tsv", trainer_ranks, config.TOUR_RECORD_HEADER)


    # Returns an array of trainers and their scores from passed tournament
    competitor_points(trainer_ranks)




    input("Finished!")

main()