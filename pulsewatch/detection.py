import statistics


def z_score(value, history):
    avg = statistics.mean(history)
    wobble = statistics.pstdev(history)
    if wobble == 0:
        return 0
    return (value - avg) / wobble