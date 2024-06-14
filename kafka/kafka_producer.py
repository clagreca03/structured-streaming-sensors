from confluent_kafka import Producer
import json
import yaml



def get_config():

    with open("config.yml") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    config = config.get('kafka-config').get('local')
    kconfig = {
        "bootstrap.servers": config.get('bootstrap.servers'),
    }

    return kconfig


# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event topic '{topic}': key = '{key}', value = '{value}'".format(
            topic=msg.topic(), key=msg.key(), value=msg.value().decode('utf-8')
        ))


if __name__ == '__main__':
    config = get_config()

    # Create Producer instance
    p = Producer(config)
    topic = 'sensor-data'
    sensors = [{"event_id": "5bb5f370-d26b-4a3f-8601-3b67ef07f19f", "event_time": "2024-06-13T22:10:23.315639", "sensor_id": 700, "sensor_name": "test350", "sensor_type": "gps", "latitude": 28.818898691074864, "longitude": -82.30191984738413}]

    for sensor in sensors:
        p.produce(topic, json.dumps(sensor).encode('utf-8'), callback=delivery_callback)

    # Block until the messages are sent.
    p.poll(10000)
    p.flush()