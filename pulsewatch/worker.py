import redis 


r = redis.Redis(host="localhost", port=6379, decode_responses=True)
last_id = "$"

while True:
    response = r.xread({"metrics": last_id}, block=5000)
    for stream_name, messages in response :
        for message_id, fields in messages :
            print (message_id, fields)
            last_id = message_id




