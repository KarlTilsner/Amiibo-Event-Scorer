import config



def competitor_points(trainer_ranks):
    competitors = {}

    # Get all unique trainers
    for entry in trainer_ranks:
        trainer = entry[1].split(" - ", 1)[0].strip()

        if trainer not in competitors:
            competitors[trainer] = 0

    # Score each entry
    for entry in trainer_ranks:
        trainer, score = points_earned(entry)
        competitors[trainer] += score

    print(competitors)

    return competitors



def points_earned(entry):
    rank = entry[0]
    trainer = entry[1].split(" - ", 1)[0].strip()
    tour_len = entry[2]

    return trainer, 1