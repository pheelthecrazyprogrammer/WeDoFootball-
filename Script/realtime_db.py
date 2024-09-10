import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient, DESCENDING
from datetime import timedelta, timezone

# MQTT settings
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_TEMPLATE_VELOCITY = 'football/players/{}/realtime/average_velocity'
MQTT_TOPIC_TEMPLATE_DISTANCE = 'football/players/{}/realtime/distance_traveled'
MQTT_TOPIC_TEMPLATE_CALORIES = 'football/players/{}/realtime/calories_consumed'

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "footballDB"
BASE_COLLECTION_NAME = "simulations"

# MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

rome_timezone = timezone(timedelta(hours=2))

def get_latest_collection():
    # Get all collection names
    collection_names = db.list_collection_names()
    # Filter for simulation collections
    simulation_collections = [name for name in collection_names if name.startswith(BASE_COLLECTION_NAME)]
    
    if not simulation_collections:
        print("No simulation data found.")
        return None
    
    # Find the latest collection by sorting
    latest_collection = max(simulation_collections)
    return latest_collection

def calculate_metrics(collection_name):
    try:
        collection = db[collection_name]

        # Query to calculate metrics for each player
        metrics = {}
        for player_id in range(1, 12):
            # Calculate average velocity
            pipeline_avg_velocity = [
                {"$match": {"player_id": player_id}},
                {"$group": {"_id": None, "avg_velocity": {"$avg": "$gps.velocity"}}}
            ]
            avg_velocity_result = list(collection.aggregate(pipeline_avg_velocity))
            avg_velocity = avg_velocity_result[0]["avg_velocity"] if avg_velocity_result else 0.0

            # Get last record for velocity and elapsed time
            pipeline_last_record = [
                {"$match": {"player_id": player_id}},
                {"$sort": {"timestamp": DESCENDING}},
                {"$limit": 1}
            ]
            last_record_result = list(collection.aggregate(pipeline_last_record))
            if last_record_result:
                last_velocity = last_record_result[0]["gps"]["velocity"]
                last_elapsed_time = last_record_result[0]["elapsed_time"]
                distance_traveled = last_velocity * (last_elapsed_time / 60.0)  # Convert minutes to hours for km
                distance_km = round(distance_traveled, 2)
            else:
                distance_km = 0.0

            # Calculate total calories consumed
            pipeline_total_calories = [
                {"$match": {"player_id": player_id}},
                {"$group": {"_id": None, "total_calories": {"$sum": "$calories_consumed.calories"}}}
            ]
            total_calories_result = list(collection.aggregate(pipeline_total_calories))
            total_calories = total_calories_result[0]["total_calories"] if total_calories_result else 0.0

            # Add metrics to the dictionary
            metrics[player_id] = {
                "average_velocity": round(avg_velocity, 2),
                "distance_traveled_km": distance_km,
                "calories_consumed": round(total_calories, 2)
            }

        return metrics

    except Exception as e:
        print(f"Error querying MongoDB: {e}")
        return None

def publish_metrics(metrics):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_start()

    for player_id, data in metrics.items():
        # Publish average velocity
        topic_velocity = MQTT_TOPIC_TEMPLATE_VELOCITY.format(player_id)
        message_velocity = json.dumps({"average_velocity": data["average_velocity"]})
        mqtt_client.publish(topic_velocity, message_velocity)
        print(f"Published average velocity for Player {player_id}: {data['average_velocity']} km/h")

        # Publish distance traveled
        topic_distance = MQTT_TOPIC_TEMPLATE_DISTANCE.format(player_id)
        message_distance = json.dumps({"distance_traveled_km": data["distance_traveled_km"]})
        mqtt_client.publish(topic_distance, message_distance)
        print(f"Published distance traveled for Player {player_id}: {data['distance_traveled_km']} km")

        # Publish calories consumed
        topic_calories = MQTT_TOPIC_TEMPLATE_CALORIES.format(player_id)
        message_calories = json.dumps({"calories_consumed": data["calories_consumed"]})
        mqtt_client.publish(topic_calories, message_calories)
        print(f"Published calories consumed for Player {player_id}: {data['calories_consumed']} cal")

    mqtt_client.loop_stop()
    mqtt_client.disconnect()

def main():
    latest_collection = get_latest_collection()
    if latest_collection:
        # Calculate metrics from the latest collection
        metrics = calculate_metrics(latest_collection)
        if metrics:
            # Publish metrics via MQTT
            publish_metrics(metrics)
        else:
            print("No metrics calculated.")
    else:
        print("No latest collection found.")

if __name__ == '__main__':
    main()
