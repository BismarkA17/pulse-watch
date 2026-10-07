import statistics


def z_score(value, history):
    avg = statistics.mean(history)
    wobble = statistics.pstdev(history)
    if wobble == 0:
        return 0
    return (value - avg) / wobble

def is_anomaly(value, history):
    if len(history) < 20 :
        return False
    z = z_score (value, history)
    if abs(z) > 3 :
        return True 
    else: 
        return False