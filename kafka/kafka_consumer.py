from confluent_kafka import Consumer
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
        "group.id": config.get('group.id'),
        "session.timeout.ms": config.get('session.timeout.ms'),
        "auto.offset.reset": config.get('auto.offset.reset'),
        "enable.auto.commit": config.get('enable.auto.commit'),
        "auto.commit.interval.ms": config.get('auto.commit.interval.ms'),
        "api.version.request": config.get('api.version.request'),
    }

    return kconfig


if __name__ == '__main__':

    config = get_config()

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    topic = "sensor-data"
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                print("Consumed event from topic '{topic}': key = '{key}', value = '{value}'".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()



