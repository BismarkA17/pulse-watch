import time
import random
import redis
from pulsewatch.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
service_list = ["checkout","auth","search"]


def make_metric(service):
    latency = random.gauss(120,15)
    error_rate = max(0,random.gauss(0.01,0.005))
    if random.random() < 0.02:
        latency = latency * 5
        error_rate = 0.3
    return {
        "service": service,          
        "latency_ms": round(latency,2),
        "error_rate": round(error_rate,4),
        "timestamp": time.time(),
    }


while True:
    for service in service_list:
        metric = make_metric(service)
        message_id = r.xadd("metrics", metric)
        print("Sent", metric, "as", message_id)
    time.sleep(1)