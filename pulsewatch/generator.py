import time

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

metric = {
    "service": "checkout",
    "latency_ms": 120.5,
    "error_rate": 0.01,
    "timestamp": time.time(),
}

message_id = r.xadd("metrics", metric)
print("Sent", metric, "as", message_id)