from random import choice
from confluent_kafka import Producer 

conf = {
    'bootstrap.servers': 'localhost:29092',
}

# Create Producer instance
p = Producer(conf)


# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event topic '{topic}': key = '{key}', value = '{value}'".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')
        ))


# Produce data by selecting random values from these lists
topic = 'quickstart-events'
user_ids = ['eabara', 'jsmith', 'sgarcia', 'jbernard', 'htanaka', 'awalther']
products = ['book', 'alarm clock', 't-shirts', 'gift card', 'batteries']

count = 0
for _ in range(10):
    user_id = choice(user_ids)
    product = choice(products)
    p.produce(topic, product, user_id, callback=delivery_callback)
    count += 1

# Block until the messages are sent.
p.poll(10000)
p.flush()