import statistics



def z_score(value, history):
    avg = statistics.mean(history)
    wobble = statistics.pstdev(history)
    return (value - avg) / wobble