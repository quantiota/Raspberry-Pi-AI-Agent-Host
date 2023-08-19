## BME680 Sensor Data Collector

### Overview

This script interfaces with the BME680 environmental sensor, retrieves its readings, and saves the data into a QuestDB database. It covers temperature, humidity, pressure, and gas resistance readings.

##  Database Setup:

The script is set to connect to a QuestDB instance with the following credentials:

```
dbname="qdb",
user="admin",
password="quest",
host="docker_host_ip_address",
port="8812"
```

Remember to replace <docker_host_ip_address> with the actual IP address of the Docker host where your server is running

