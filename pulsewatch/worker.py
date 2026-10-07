import redis 
import psycopg
from pulsewatch.detection import is_anomaly

conn = psycopg.connect(
    "postgresql://pulsewatch:pulsewatch@localhost:5432/pulsewatch",
    autocommit=True,
)


r = redis.Redis(host="localhost", port=6379, decode_responses=True)
last_id = "$"
histories = {}

while True:
    response = r.xread({"metrics": last_id}, block=5000)
    for stream_name, messages in response :
        for message_id, fields in messages :
            service = fields["service"]
            latency = float(fields["latency_ms"])
            error_rate = float(fields["error_rate"])
            timestamp = float(fields["timestamp"])


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
            history.append(latency)
            if len(history) > 30 : 
                history.pop(0)
            
            print("Saved", service, latency, error_rate)
            last_id = message_id




