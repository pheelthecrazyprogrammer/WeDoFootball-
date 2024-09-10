# WeDoFootball-
This project involves developing a system to track soccer players' movements, vital signs, and calories using sensors integrated with digital devices. A GUI displays real-time match data, including a heat map for tactical analysis. An integrated database enables data storage and advanced insights for coaches, players, and fans.

# WeDoFootball! - README
Project Overview
WeDoFootball! is a simulation system designed to track soccer players' movements, vital signs (pressure, body temperature, heart rate), and calories burned using sensors integrated with digital devices. The system features a user-friendly GUI that displays real-time match data, including heatmaps of player movements, enabling tactical analysis. An integrated MongoDB database supports data storage and advanced analytics for insights that benefit coaches, players, and fans.

# Key Components
Simulators: Generate simulated sensor data for players over a 90-second period (equivalent to a 90-minute match). Data includes metrics like heart rate, GPS position, and calories consumed.

 - MQTT Broker: Handles real-time communication between simulators and the dashboard using pre-defined topics.
 - Node-RED Dashboard: A visual interface to display real-time data from the MQTT broker, including charts, heatmaps, and player statistics.
 - MongoDB Integration: Stores simulation data and enables advanced analytics for performance metrics like average speed and distance traveled.

# Setup Instructions
Install Dependencies:
Python libraries: paho-mqtt, pymongo, Node-RED, and others as needed.
MongoDB for data storage.
Node-RED for real-time visualization.
Run Simulators:

Execute simulators.py to generate sensor data.
Ensure MQTT broker is running on localhost:1883.
Configure MQTT Broker:

Set MQTT_BROKER, MQTT_PORT, and topic templates in the script configuration.
Use predefined topics to subscribe to players’ sensor data and coordinate topics.

MongoDB Setup:
Ensure MongoDB is running locally on port 27017.
Define database and collection names for storing simulation data.

Run Node-RED:
Use the provided flows.json to configure Node-RED for data retrieval and dashboard setup.
Access the dashboard to monitor real-time match data.

# Key Functions
Data Generation: Generates player metrics based on their roles and match progression.
Real-Time Data Publishing: Publishes sensor data to the MQTT broker and stores it in MongoDB.
Dashboard Visualization: Displays real-time match statistics, including a heatmap for player positions.

# Future Enhancements
Add advanced analytics using machine learning for predicting player performance.
Integrate with wearable devices for more accurate data collection.

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**.

You are free to:
- Share — copy and redistribute the material in any medium or format.

Under the following terms:
- **Attribution** — You must give appropriate credit to the original authors of this project.
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, or build upon the material, you may not distribute the modified material.

For more details, see the [LICENSE](LICENSE) file.
