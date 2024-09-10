import time
import json
import random
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

# MQTT settings
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_TEMPLATE = 'football/players/{}/sensors'
MQTT_COORDINATES_TOPIC_TEMPLATE = 'football/players/{}/sensors/coordinates'

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "footballDB"
BASE_COLLECTION_NAME = "simulations"

# Definition of roles and player distribution
ROLES = {
    1: 'portiere',
    2: 'difensore',
    3: 'difensore',
    4: 'difensore',
    5: 'difensore',
    6: 'centrocampista',
    7: 'centrocampista',
    8: 'centrocampista',
    9: 'attaccante',
    10: 'attaccante',
    11: 'attaccante'
}

# MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

rome_timezone = timezone(timedelta(hours=2))

def generate_metrics(player_id, role, elapsed_time):
    # Coefficients to modify player behavior towards the end of the simulation
    if elapsed_time > 80:
        heart_rate_coefficient = 1.1  # Increase heart rate
        gps_velocity_coefficient = 0.5  # Reduce movement speed
    else:
        heart_rate_coefficient = 1.0
        gps_velocity_coefficient = 1.0

    if role == 'portiere':
        return {
            "player_id": player_id,
            "role": role,
            "heart_rate": {"heart_rate": int(random.randint(120, 180) * heart_rate_coefficient)},
            "temperature": {"body_temperature": round(random.uniform(35.5, 38), 1)},
            "blood_pressure": {"systolic": random.randint(170, 230), "diastolic": random.randint(75, 95)},
            "calories_consumed": {"calories": round(random.uniform(10, 13), 1)},
            "gps": {"x": random.randint(0, 30), "y": random.randint(25, 40), "velocity": round(random.uniform(0, 6) * gps_velocity_coefficient, 1), "unic": random.randint(0, 700)},
            "timestamp": datetime.now(rome_timezone).isoformat(),
            "elapsed_time": elapsed_time
        }
    elif role == 'difensore':
        return {
            "player_id": player_id,
            "role": role,
            "heart_rate": {"heart_rate": int(random.randint(120, 180) * heart_rate_coefficient)},
            "temperature": {"body_temperature": round(random.uniform(35.5, 38.0), 1)},
            "blood_pressure": {"systolic": random.randint(170, 230), "diastolic": random.randint(75, 95)},
            "calories_consumed": {"calories": round(random.uniform(10, 20), 1)},
            "gps": {"x": random.randint(5, 52), "y": random.randint(0, 65), "velocity": round(random.uniform(0, 15) * gps_velocity_coefficient, 1), "unic": random.randint(0, 1706)},

            "timestamp": datetime.now(rome_timezone).isoformat(),
            "elapsed_time": elapsed_time
        }
    elif role == 'centrocampista':
        return {
            "player_id": player_id,
            "role": role,
            "heart_rate": {"heart_rate": int(random.randint(120, 180) * heart_rate_coefficient)},
            "temperature": {"body_temperature": round(random.uniform(35.5, 38.0), 1)},
            "blood_pressure": {"systolic": random.randint(170, 230), "diastolic": random.randint(75, 95)},
            "calories_consumed": {"calories": round(random.uniform(10, 20), 1)},
            "gps": {"x": random.randint(30, 80), "y": random.randint(0, 65), "velocity": round(random.uniform(0, 17) * gps_velocity_coefficient, 1), "unic": random.randint(1706, 5118)},
            "timestamp": datetime.now(rome_timezone).isoformat(),
            "elapsed_time": elapsed_time
        }
    elif role == 'attaccante':
        return {
            "player_id": player_id,
            "role": role,
            "heart_rate": {"heart_rate": int(random.randint(120, 180) * heart_rate_coefficient)},
            "temperature": {"body_temperature": round(random.uniform(35.5, 38.0), 1)},
            "blood_pressure": {"systolic": random.randint(170, 230), "diastolic": random.randint(75, 95)},
            "calories_consumed": {"calories": round(random.uniform(10, 20), 1)},
            "gps": {"x": random.randint(50, 105), "y": random.randint(5, 60), "velocity": round(random.uniform(0, 17) * gps_velocity_coefficient, 1), "unic": random.randint(3412, 3412*2)},
            "timestamp": datetime.now(rome_timezone).isoformat(),
            "elapsed_time": elapsed_time
        }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker with result code {rc}")
        # Subscribe to topics for all players
        for player_id in range(1, 12):  # Range from 1 to 11 (inclusive)
            client.subscribe(MQTT_TOPIC_TEMPLATE.format(player_id))
    else:
        print(f"Failed to connect to MQTT broker with result code {rc}")

def on_message(client, userdata, msg):
    for player_id, role in ROLES.items():
        topic = MQTT_TOPIC_TEMPLATE.format(player_id)
        if msg.topic == topic:
            data = json.loads(msg.payload.decode())
            # Create a simplified message with only x and y coordinates
            simplified_data = {
                "player_id": data["player_id"],
                "role": data["role"],
                "gps": {
                    "x": data["gps"]["x"],
                    "y": data["gps"]["y"]
                }
            }
            # Publish simplified data to coordinates topic
            coordinates_topic = MQTT_COORDINATES_TOPIC_TEMPLATE.format(player_id)
            client.publish(coordinates_topic, json.dumps(simplified_data))
            print(f"Published coordinates for Player {player_id} to topic '{coordinates_topic}'")

def store_simulation_data(simulation_name, data):
    collection_name = f"{BASE_COLLECTION_NAME}_{simulation_name}"
    collection = db[collection_name]
    try:
        collection.insert_one(data)
        print(f"Data inserted into MongoDB collection '{collection_name}': {data}")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")

def main():
    mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Specify MQTT protocol version
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

    mqtt_client.loop_start()  # Start a background thread to handle MQTT events

    try:
        elapsed_time = 0  # Initialize the simulation elapsed time
        simulation_name = datetime.now(rome_timezone).strftime("%Y%m%d_%H%M%S")  # Generate a unique name for the simulation

        while elapsed_time <= 90:  # Simulate a football match duration (90 minutes)
            for player_id in range(1, 12):  # Range from 1 to 11 (inclusive)
                role = ROLES[player_id]
                payload = generate_metrics(player_id, role, elapsed_time)

                mqtt_topic = MQTT_TOPIC_TEMPLATE.format(player_id)
                mqtt_client.publish(mqtt_topic, json.dumps(payload))
                store_simulation_data(simulation_name, payload)
                print(f"Published and stored data for Player {player_id} ({role})")

            elapsed_time += 1  # Increment elapsed time
            time.sleep(1)  # Simulate one second of real time

    except KeyboardInterrupt:
        print("\nStopping sensor simulation...")
        mqtt_client.loop_stop()  # Stop the MQTT thread
        mqtt_client.disconnect()

if __name__ == '__main__':
    main()
