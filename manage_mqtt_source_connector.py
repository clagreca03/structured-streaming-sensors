import requests
import json
import argparse
import yaml



def create_connector(url):
    """ Create a new MQTT source connector into Kafka """

    # Set the JSON body for the request
    json_file_path = config.get('mqtt.source.connector.file')
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    # Make the POST request to create the connector
    headers = {"Content-Type": "application/json"}
    response = requests.post(url + "/connectors", headers=headers, data=json.dumps(json_data))

    if response.status_code == 201:
        print("Connector created successfully")
    else:
        print(f"Failed to create connector. Status code: {response.status_code}")
        print(f"Response: {response.text}")


def delete_connector(url):
    """ Delete an existing MQTT source connector from Kafka """

    # Set the JSON body for the request
    json_file_path = config.get('mqtt.source.connector.file')
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    headers = {"Content-Type": "application/json"}
    response = requests.delete(url + f"/connectors/{json_data['name']}", headers=headers)

    if response.status_code == 204:
        print("Connector deleted successfully")
    else:
        print(f"Failed to delete connector. Status code: {response.status_code}")
        print(f"Response: {response.text}")



def get_config():

    with open("config.yml") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    return config



def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs='?', help="select action (create, delete)", default="create")
    args = parser.parse_args()


    if args.action:
        action = str(args.action)
    else:
        print("Please specify the action to perform")
        exit()

    return action


if __name__ == "__main__":

    action = parse_arguments()
    c = get_config()
    env = c.get('global-env')
    config = c.get('kafka-config').get(env)

    kafka_url = config.get('kafka.connect.url')


    if action == "create":
        create_connector(kafka_url)

    elif action == "delete":
        delete_connector(kafka_url)