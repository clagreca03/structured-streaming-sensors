import paho.mqtt.client as paho
import time
import json
import argparse
import yaml


def on_connect(client, userdata, flags, reason_code, properties=None):

    print(f"Connected with reason code: {reason_code}")
    client.subscribe(config.get('mqtt.topic'))
    

def on_message(client, userdata, message):
    
    print('\n')
    payload = json.loads(message.payload.decode("utf-8"))
    print(f"Topic: {message.topic}\nPayload: {payload}")


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
    args = parser.parse_args()

    if args.env:
        env = str(args.env)
    else:
        print("Please specify the number of events to generate")
        exit()

    return env


if __name__ == '__main__':
    
    env = parse_arguments()
    config = get_config().get('mqtt-config').get(env)


    client = paho.Client(paho.CallbackAPIVersion.VERSION2, client_id=config.get('mqtt.client.id'))
    if config.get('mqtt.require.login'): client.username_pw_set(username=config.get('mqtt.user'), password=config.get('mqtt.pass'))
    
    # register callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    if config.get('mqtt.tls'): client.tls_set()
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
    