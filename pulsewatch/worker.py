import redis 
import psycopg
from pulsewatch.detection import is_anomaly
from pulsewatch.config import DATABASE_URL, REDIS_URL

def parse_message(fields):
    service = fields["service"]
    latency = float(fields["latency_ms"])
    error_rate = float(fields["error_rate"])
    timestamp = float(fields["timestamp"])
    return service, latency, error_rate, timestamp

def update_history(history, value):
    history.append(value)
    if len(history) > 30 :
        history.pop(0)

def process_message(conn, histories, fields):
    service, latency, error_rate, timestamp = parse_message(fields)
    conn.execute(
        "INSERT INTO metrics(service, latency_ms, error_rate, recorded_at)"
        "VALUES (%s, %s, %s, to_timestamp(%s))",
        (service, latency, error_rate, timestamp),
    )
    if service not in histories:
        histories[service] = []
    history = histories[service]
    
    if is_anomaly(latency, history):
        print (f"Anomaly detected: {service}  {latency}")
        conn.execute(
            "INSERT INTO incidents(service, latency_ms)"
            "VALUES(%s, %s)",
            (service,latency)
        )
    update_history(history, latency)
    print("Saved", service, latency, error_rate)



def main():

    conn = psycopg.connect(
        DATABASE_URL,
        autocommit=True,
    )


    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        r.xgroup_create("metrics", "workers", id="$", mkstream=True)
    except redis.exceptions.ResponseError:
        pass

    #last_id = "$"
    histories = {}

    while True:
        response = r.xreadgroup("workers", "worker-1", {"metrics": ">"}, block=5000)
        for stream_name, messages in response :
            for message_id, fields in messages :
                process_message(conn, histories, fields)
                r.xack("metrics", "workers", message_id)

if __name__ == "__main__":
    main()




