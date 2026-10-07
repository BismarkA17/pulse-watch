import redis 
import psycopg

conn = psycopg.connect(
    "postgresql://pulsewatch:pulsewatch@localhost:5432/pulsewatch",
    autocommit=True,
)


r = redis.Redis(host="localhost", port=6379, decode_responses=True)
last_id = "$"

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
            print("Saved", service, latency, error_rate)
            last_id = message_id




