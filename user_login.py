import random
from confluent_kafka import Producer
import time
import json

def generate_user_login_event(user_id):
    event = {
        'event_type':'login',
        'user_id': user_id,
        'timestamp': int(time.time())
    }
    return event

producer = Producer({
    'bootstrap.servers': '87.236.23.232:9092'
})

users = ['user1', 'user2', 'user3']

while True:
    user_id = random.choice(users)
    event = generate_user_login_event(user_id)
    producer.produce(topic='user_logins', value=json.dumps(event).encode('utf-8'))
    producer.poll(0)
    time.sleep(random.randint(5, 15))
    producer.flush()