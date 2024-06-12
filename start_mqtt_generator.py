import paho.mqtt.client as paho
import json
import time
import argparse
import yaml

from data_generator.gps_sensor_data import generate_sensor_data
    

def on_connect(client, userdata, flags, reason_code, properties=None):
    
    print(f"Connected with reason code: {reason_code}")


def get_config():

    with open("config.yml") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    return config

   
def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("events", help="number of events to generate")
    parser.add_argument("sensors", nargs='?', help="number of unique sensors", default=1)
    args = parser.parse_args()


    if args.events:
        events = int(args.events)
    else:
        print("Please specify the number of events to generate")
        exit()

    if args.sensors:
        sensors = int(args.sensors)
    else:
        print("Please specify the number of sensors to generate")
        exit()

    return events, sensors
 

if __name__ == '__main__':

    events, sensors = parse_arguments()
    c = get_config()
    env = c.get('global-env')
    config = c.get('mqtt-config').get(env)
    sensor_data = generate_sensor_data(events, sensors)

    client = paho.Client(paho.CallbackAPIVersion.VERSION2, client_id=config.get('mqtt.geneator.client.id'))
    if config.get('mqtt.require.login'): client.username_pw_set(username=config.get('mqtt.user'), password=config.get('mqtt.pass'))

    # register callbacks
    client.on_connect = on_connect

    if config.get('mqtt.tls'): client.tls_set()
    print(f"Connecting to the MQTT broker {config.get('mqtt.server')} on port {config.get('mqtt.port')}")
    client.connect(config.get('mqtt.server'), config.get('mqtt.port'))
    client.loop_start()

    topic = config.get('mqtt.topic')

    try:
        for s in sensor_data:
            result = client.publish(topic, json.dumps(s))
            print(f"Published with result: {result} \n{s}")
            time.sleep(1)  
    except KeyboardInterrupt:
        pass  
    finally:
        client.disconnect()
        client.loop_stop()



