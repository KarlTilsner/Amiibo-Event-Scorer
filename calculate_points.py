import config
from tsv import openTSV, writeTSV, getAllInFolder



def compile_points():
    filepaths = getAllInFolder()
    total_points = {}

    for path in filepaths:
        # Returns a dictionary of trainers and their scores from passed tournament
        tour_points = competitor_points(openTSV(path))

        for trainer, points in tour_points.items():
            total_points[f"{trainer}"] = total_points.get(f"{trainer}", 0) + points

    total_points = dict(sorted(total_points.items(), key=lambda item: item[1], reverse=True))

    tsv_data = []
    for i, (trainer, points) in enumerate(total_points.items(), start=1):
        tsv_data.append([i, trainer, points])
    
    writeTSV("Competitor Points.tsv", tsv_data, config.COMPETITOR_POINTS_HEADER)

    input("Finished! Press any key to return to the menu.")
    return



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







# WIP: Will be used to determine how many points a host will earn for their tournament.
def host_points_earned(entry, amiibo_count):
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
        modifier = (tour_len - expected_matches) * 0.2

    points = 0
    if f"{rank}" in config.base_points[f"{points_bracket}"]:
        points = int(config.base_points[f"{points_bracket}"][f"{rank}"] + modifier)

    return trainer, points