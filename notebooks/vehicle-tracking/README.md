## SIM7600E-H 4G HAT GPS Tracker

### Overview

This script is designed to interact with the SIM7600E-H 4G HAT GPS module to retrieve GPS location data and store it in a QuestDB database. It establishes a connection to the database, creates a table if it doesn't exist, and sets up the serial communication with the GPS module. The script continuously queries the GPS module for its information using AT commands and extracts relevant GPS parameters such as latitude, longitude, altitude, speed, and timestamp. These parameters are then transformed and formatted for better readability. The latitude and longitude values are calculated from degree and minute components and stored in the database along with other extracted information. Any errors encountered during the process are gracefully handled, and the serial port and database connection are properly closed at the end. The script offers an efficient and reliable way to capture and manage GPS data from the SIM7600E-H 4G HAT GPS module

###  Set up parameter:

The script is set to connect to a QuestDB instance with the following credentials:

```
dbname="qdb",
user="admin",
password="quest",
host="docker_host_ip_address",
port="8812"
```

Remember to replace **<docker_host_ip_address>** with the actual IP address of the Docker host where your server is running

### GPS Tracker Data query

```
-- Retrieve the timestamp and data values: latitude, longitude, altitude, speed.

SELECT
    timestamp,        -- Select the timestamp of the data
    data              -- Select the data value
FROM  
    gps_data      -- From the 'gps_data' table
WHERE 
    timestamp > dateadd('d', -1, now()); -- Only select data from the past 24 hours

```

This Grafana query retrieves the timestamp and corresponding data values from the **gps_data** table. It's specifically designed to only fetch data from the last 24 hours, ensuring that dashboard viewers are presented with the most recent day's data trends. By focusing on this short timeframe, users can gain insights into daily data fluctuations and patterns, which can be especially valuable for real-time monitoring or short-term data analysis.

### Dashboard



![GPS Tracker Dashboard](./gps_tracker_dashboard.png)