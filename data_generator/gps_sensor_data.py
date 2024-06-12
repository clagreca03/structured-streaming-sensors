from faker import Faker
import random
from datetime import datetime, timedelta
import pprint


# Initialize Faker
fake = Faker()


def generate_sensors(unique_sensors: int):
    fake = Faker()
    sensors = [{
        'sensor_id': fake.pyint(100, 999),
        # 'latitude': random.uniform(24.396308, 49.384358),  # US latitude range
        # 'longitude': random.uniform(-125.0, -66.93457)     # US longitude range
        'latitude': random.uniform(27.5, 29.5),  # Central Florida latitude range
        'longitude': random.uniform(-82.5, -80.5)  # Central Florida longitude range
    } for _ in range(unique_sensors)]
    return sensors


def adjust_sensor_position(latitude, longitude):

    # Adjust latitude and longitude slightly to simulate movement
    new_latitude = latitude + random.uniform(-0.05, 0.05) # small random offset
    new_longitude = longitude + random.uniform(-0.05, 0.05) # small random offset

    return new_latitude, new_longitude


def generate_sensor_data(events: int, unique_sensors: int = 1): 
    sensors = generate_sensors(unique_sensors)
    sensor_data = []

    for _ in range(events):
        sensor = random.choice(sensors)
        new_latitude, new_longitude = adjust_sensor_position(sensor['latitude'], sensor['longitude'])

        sensor_event = {
            'event_id': fake.uuid4(), 
            'event_time': (datetime.now() + timedelta(seconds=10*_)).isoformat(),  # Incremental timestamps => use this for Faker fake.iso8601(),
            'sensor_id': sensor['sensor_id'],
            'sensor_name': 'test' + str(fake.pyint(100, 999)),
            'sensor_type': 'gps',
            'latitude': new_latitude,  # US latitude range
            'longitude': new_longitude     # US longitude range
        }

        # Update sensor's curernt position
        sensor['latitude'] = new_latitude
        sensor['longitude'] = new_longitude

        sensor_data.append(sensor_event)

    return sensor_data



# sensor_list = generate_sensors(10)
# pprint.pp(sensor_list)

# sensor_data = generate_sensor_data(100, 10)
# pprint.pp(sensor_data)