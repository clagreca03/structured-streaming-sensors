import paho.mqtt.client as paho
import time
import json
import argparse
import yaml


def on_connect(client, userdata, flags, reason_code, properties=None):
    """ Callback function for the on_connect event """

    if reason_code == 0:
        print(f"Connected with reason code: {reason_code}")
        client.subscribe(config.get('mqtt.topic'))
    else:
        print(f"Connection failed with reason code: {reason_code}")


def on_subscribe(client, userdata, mid, reason_code, properties=None):
    """ Callback function for the on_subscribe event """

    print(f"Successfully subscribed to topics...")

    
def on_message(client, userdata, message):
    """ Callback function for the on_message event """
    
    print('\n')
    payload = json.loads(message.payload.decode("utf-8"))
    print(f"Topic: {message.topic}\nPayload: {payload}")


def on_log(client, userdata, level, buf):
    """ Callback function for the on_log event """

    print(f"Level: {level}, Message: {buf}")


def get_config():

    with open("config.yml") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    return config


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("env", help="select mqtt environment")
    parser.add_argument("topic", nargs='?', help="(optional) select mqtt topic", default=None)
    args = parser.parse_args()

    if args.env:
        env = str(args.env)
    else:
        print("Please specify the mqtt environment") 
        exit()

    if args.topic:
        topic = str(args.topic)



    return args


if __name__ == '__main__':
    
    args = parse_arguments()
    env, topic = args.env, args.topic
    config = get_config().get('mqtt-config').get(env)

    # if the topic argument is not specified, use the default topic
    if config is None:
        print("Something went wrong with your config selection. Please try again.")
        exit()
    else:
        config['topic'] = topic

    # create a client instance
    client = paho.Client(paho.CallbackAPIVersion.VERSION2, client_id=config.get('mqtt.client.id'))
    if config.get('mqtt.require.login'): client.username_pw_set(username=config.get('mqtt.user'), password=config.get('mqtt.pass'))
    if config.get('mqtt.tls'): client.tls_set()
    

    # register callbacks
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    # connect optional parameters
    # client.on_log = on_log

    print(f"Connecting to the MQTT broker {config.get('mqtt.server')} on port {config.get('mqtt.port')}")
    client.connect(config.get('mqtt.server'), config.get('mqtt.port'))
    client.loop_start()

    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
        client.loop_stop()
    