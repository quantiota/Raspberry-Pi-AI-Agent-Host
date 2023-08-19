## BME680 Sensor Data Collector

### Overview

This script interfaces with the BME680 environmental sensor, retrieves its readings, and saves the data into a QuestDB database. It covers temperature, humidity, pressure, and gas resistance readings.

### Prerequisites

- **Python 3**: This script is written in Python 3. Ensure you have it installed.
- **Python Libraries**:
    - **bme680**: To interface with the BME680 sensor.
    - **psycopg2**: To communicate with the PostgreSQL database.
- **QuestDB**: Ensure you have a running QuestDB instance.

### Setup

1. **Install Required Libraries**:
Use the following command to install the necessary Python libraries:

Copy code
pip install bme680 psycopg2

2. **Database Setup**:

The script is set to connect to a PostgreSQL instance with the following credentials:


dbname="qdb",
user="admin",
password="quest",
host="docker_host_ip_address",
port="8812"

Remember to replace <docker_host_ip_address> with the actual IP address of the Docker host where your server is running

3. **Sensor Connection**:
Connect the BME680 sensor to your device. The script attempts to connect to the primary I2C address first. If unsuccessful, it falls back to the secondary address.

### Running the Script

Navigate to the directory containing the script and run:


$ data-stream-processing.py


### Understanding the Output

Upon running, the script:

1. Outputs calibration data for the BME680 sensor. This is purely informational and can be commented out if not desired.
2. Enters an infinite loop, collecting sensor data every 60 seconds.
3. Each reading is saved to the weather_data table in the PostgreSQL database and printed to the console.

### Troubleshooting

- If the script fails to connect to the BME680 sensor, ensure it's connected correctly and the appropriate drivers are installed.
- Ensure your PostgreSQL service is running and accepting connections.
- Double-check the database credentials within the script.
