import requests
import json
import argparse
import yaml



def create_index():
    """ Create an index in Elastic """

    with open("./kibana/sensor-data.json") as f:
        json_data = json.load(f)

    # Make the POST request to create the Elastic index
    headers = {"Content-Type": "application/json"}
    response = requests.put(elastic_url + "/sensor-data", headers=headers, data=json.dumps(json_data))

    if response.status_code == 200:
        print("Index created successfully")
    else:
        print(f"Failed to create index. Status code: {response.status_code}")
        print(f"Response: {response.text}")


def clear_index():
    """ Clear an index in Elastic """

    json_data = {'query': {'match_all': {}}}

    headers = {"Content-Type": "application/json"}
    response = requests.post(elastic_url + "/sensor-data/_delete_by_query", headers=headers, data=json.dumps(json_data))

    if response.status_code == 200:
        print("Index cleared successfully")
    else:
        print(f"Failed to clear index. Status code: {response.status_code}")
        print(f"Response: {response.text}")


def delete_index():
    """ Delete an index in Elastic """

    response = requests.delete(elastic_url + "/sensor-data")

    if response.status_code == 200:
        print("Index deleted successfully")
    else:
        print(f"Failed to delete connector. Status code: {response.status_code}")
        print(f"Response: {response.text}")


def create_data_view():
    """ Create a data view in Kibana """

    with open("./kibana/sensor-data-view.json") as f:
        json_data = json.load(f)

    headers = {"kbn-xsrf": "true"}
    response = requests.post(kibana_url + "/api/data_views/data_view", headers=headers, data=json.dumps(json_data))

    if response.status_code == 200:
        print("Data view created successfully")
    else:
        print(f"Failed to create data view. Status code: {response.status_code}")
        print(f"Response: {response.text}")


def create_map():
    """ Import the 'Sensor Data Live' map into Kibana """

    headers = {"kbn-xsrf": "true"}
    file = "./kibana/sensor-data-map.ndjson"
    files = {'file': (file, open(file, 'rb'),'application/octet-stream')} 
    response = requests.post(kibana_url + "/api/saved_objects/_import", files=files, headers=headers)

    errors =  json.loads(response.text).get('errors')

    if response.status_code == 200 and errors is None:
        print("Map created successfully")
        print(f"Status code: {response.status_code}")
    elif response.status_code == 200 and errors is not None:
        map_id = errors[0]['id']
        print(f"Status code: {response.status_code}, cannot be trusted. The saved object of type = 'map' and id = '{map_id}' already exists.")
    else:
        print(f"Failed to create map. Status code: {response.status_code}")
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
    parser.add_argument("action", nargs='?', help="select action (create, clear, delete, or map)", default="create")
    args = parser.parse_args()


    if args.action:
        action = str(args.action)
    else:
        print("Please specify an action (create, clear, delete, map)")
        exit()

    return action


if __name__ == "__main__":

    c = get_config()
    env = c.get('global-env')
    config = c.get('elastic-config').get(env)
    action = parse_arguments()

    elastic_url = config.get('elastic.url')
    kibana_url = config.get('kibana.url')


    if action == "create":
        create_index()
        create_data_view()
        create_map()

    elif action == "clear":
        clear_index()

    elif action == "delete":
        delete_index()

    elif action == "map":
        create_map()

    else: 
        print("Invalid action. Please specify create, clear, delete, or map.")
        exit()


