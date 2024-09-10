# WeDoFootball

WeDoFootball is a cutting-edge simulation system designed to track soccer players' movements, vital signs, and calories burned using sensors integrated with digital devices. The system features real-time data visualization through a user-friendly GUI, providing tactical analysis and advanced insights. With an integrated MongoDB database, coaches, players, and fans gain valuable data-driven feedback to enhance performance.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Components](#key-components)
3. [Setup Instructions](#setup-instructions)
4. [Key Functions](#key-functions)
5. [Future Enhancements](#future-enhancements)
6. [License](#license)

## Project Overview

**WeDoFootball** tracks the following player metrics using integrated sensors:
- **Movements** (via GPS)
- **Vital Signs**: heart rate, body temperature, and blood pressure
- **Calories Burned**

The data is visualized in real-time on a **Node-RED Dashboard**, which includes a heatmap for tactical analysis and other performance metrics. Additionally, all data is stored in a **MongoDB database**, enabling advanced analytics and reporting for coaches, players, and fans.

## Key Components

- **Simulators**: 
  Simulate real-time player sensor data for a 90-second session, equivalent to a 90-minute soccer match. The simulated data includes:
  - Heart rate
  - GPS position (to generate movement heatmaps)
  - Calories burned
  
- **MQTT Broker**: 
  Facilitates real-time communication between the simulators and the dashboard. Topics are pre-defined to handle data such as players' sensor metrics and coordinates.
  
- **Node-RED Dashboard**: 
  Provides real-time data visualization through:
  - Player statistics (heart rate, calories, etc.)
  - Heatmaps for movement and positioning
  - Match statistics and charts for performance analysis
  
- **MongoDB Integration**: 
  Collects and stores simulation data in a database. This enables post-match analysis and advanced insights, such as:
  - Average speed
  - Distance traveled
  - Player-specific performance trends

## Setup Instructions

### 1. Install Dependencies:
- **Python libraries**: Install `paho-mqtt` and `pymongo` for MQTT communication and MongoDB integration.
- **Node-RED**: Required for the real-time dashboard visualization.
- **MongoDB**: Necessary for storing and retrieving match data.

To install the dependencies, run:

```bash
pip install paho-mqtt pymongo
```

### 2. Run MongoDB:
Ensure MongoDB is running locally on port `27017`.

```bash
sudo service mongod start
```

### 3. Run the MQTT Broker:
Ensure the MQTT broker is configured to run on `localhost:1883`.

### 4. Execute the Simulators:
Run the Python simulators to start generating player data:

```bash
python simulators.py
```

### 5. Configure Node-RED:
- Import the provided `flows.json` into Node-RED.
- Run Node-RED to visualize the real-time player data on the dashboard.

```bash
node-red
```

- Access the Node-RED dashboard at `http://localhost:1880/ui`.

## Key Functions

- **Data Generation**: 
  - The simulator generates player metrics based on their position and match events, creating a rich dataset for real-time visualization.
  
- **Real-Time Data Publishing**: 
  - The simulator sends sensor data to the MQTT broker, which then publishes the data to the dashboard and stores it in MongoDB.

- **Dashboard Visualization**: 
  - The Node-RED dashboard displays:
    - Heatmaps for each player’s movements
    - Live heart rate, calories burned, and other player-specific metrics
    - Tactical analysis and match performance statistics

## Future Enhancements

- **Machine Learning Integration**: 
  - Implement machine learning models to predict player performance and fatigue based on real-time data.
  
- **Wearable Device Integration**: 
  - Expand the system to integrate with actual wearable devices for more precise and real-world data collection.

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**.

You are free to:
- **Share** — copy and redistribute the material in any medium or format.

Under the following terms:
- **Attribution** — You must give appropriate credit to the original authors.
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, or build upon the material, you may not distribute the modified material.

For more details, see the [LICENSE](LICENSE) file.
