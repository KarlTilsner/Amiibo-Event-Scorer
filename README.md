# Amiibo Event Scorer
Created to drastically reduce the amount of work it takes to award event points to competitors and tournament hosts in the amiibo training community.

## Before you start
Simply enter your challonge api key and username into `config.json`. Challonge requires this in order to collect tournament results.
`"challonge_username": "your-challonge-username"`
`"challonge_api_key": "your-challonge_api_key"`

## Get tournament results
You can either collect a tournament that has one bracket, or a tournament that has multiple brackets. In the main menu, select the option that matches the tournament you wish to enter. then enter the name of the host and the challonge URL/s. A .tsv file will be saved in the folder named `Tournament Records` with either the name of the challonge bracket you entered or the name of the final bracket in the tournament (the finals or final decider bracket etc). Do not modify or move these files until the end of the event, as they are needed for calculating points for competitors and hosts.

## Calculate competitor and host points
Once you have recorded at least one tournament, you may select the options to calculate points for competitors and hosts. The points are calculated off of the tournaments currently stored in the `Tournament Records` folder. Two .tsv files will be stored in the `Spreadsheets` folder which will contain the current standings for both competitors and hosts.