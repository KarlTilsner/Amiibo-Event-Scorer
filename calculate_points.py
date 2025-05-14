import config
from tsv import openTSV, writeTSV, getAllInFolder



def competitor_points(trainer_ranks):
    amiibo_count = len(trainer_ranks)
    competitors = {}

    # Get all unique trainers
    for entry in trainer_ranks:
        trainer = entry[1].split(" - ", 1)[0].strip()

        if trainer not in competitors:
            competitors[trainer] = 0

    # Score each entry
    for entry in trainer_ranks:
        trainer, score = competitor_points_earned(entry, amiibo_count)
        competitors[trainer] += score

    return competitors



def host_points(tournament):
    amiibo_count = len(tournament)
    tour_len = int(tournament[0][2])
    host_name = tournament[0][3]

    return host_points_earned(amiibo_count, tour_len), host_name



def competitor_points_earned(entry, amiibo_count):
    rank = entry[0]
    trainer = entry[1].split(" - ", 1)[0].strip()
    tour_len = int(entry[2])

    if amiibo_count < 64:
        points_bracket = 32
    if amiibo_count >= 64 and amiibo_count < 128:
        points_bracket = 64
    if amiibo_count >= 128 and amiibo_count < 256:
        points_bracket = 128
    if amiibo_count >= 256 and amiibo_count < 512:
        points_bracket = 256
    if amiibo_count >= 512:
        points_bracket = 512

    expected_matches = points_bracket * 2 - 1
    modifier = 0
    if tour_len > expected_matches:
        modifier = (tour_len - expected_matches) * config.COMPETITOR_BONUS_POINTS

    points = 0
    if f"{rank}" in config.COMPETITOR_BASE_POINTS[f"{points_bracket}"]:
        points = int(config.COMPETITOR_BASE_POINTS[f"{points_bracket}"][f"{rank}"] + modifier)

    return trainer, points



def host_points_earned(amiibo_count, tour_len):

    if amiibo_count < 64:
        points_bracket = 32
    if amiibo_count >= 64 and amiibo_count < 128:
        points_bracket = 64
    if amiibo_count >= 128 and amiibo_count < 256:
        points_bracket = 128
    if amiibo_count >= 256 and amiibo_count < 512:
        points_bracket = 256
    if amiibo_count >= 512:
        points_bracket = 512

    expected_matches = points_bracket * 2 - 1
    modifier = 0
    if tour_len > expected_matches:
        modifier = (tour_len - expected_matches) * config.HOST_BONUS_POINTS

    points = int(config.HOST_BASE_POINTS[f"{points_bracket}"] + modifier)

    return points