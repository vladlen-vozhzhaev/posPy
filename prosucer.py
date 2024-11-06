import psutil
from confluent_kafka import Producer
import time
import json

def get_server_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        'timestamp': int(time.time()),
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage
    }
producer = Producer({
    'bootstrap.servers': '87.236.23.232:9092'
})
while True:
    metrics = get_server_metrics()
    producer.produce(
        topic='my_topic',
        value=json.dumps(metrics).encode('utf-8'),
    )
    producer.poll(0)
    time.sleep(10)
    producer.flush()


# https://site.com/img/img.jpeg?i=123213232
