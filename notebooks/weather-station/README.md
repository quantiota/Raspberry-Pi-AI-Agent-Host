## Weather Data Collector with bme680 and QuestDB


This script uses the BME680 sensor to collect weather-related data such as temperature, humidity, pressure, and gas resistance. The data is then stored in a QuestDB instance.

### Requirements

- **bme680** Python library.
- **psycopg2** Python library.
- A running instance of QuestDB with appropriate credentials.
- BME680 sensor attached to the executing system.


### Configuration
Before executing the script, ensure the following:

- The database parameters (**dbname**, **user**, **password**, **host**, and **port**) are set correctly in the script.
- The BME680 sensor is correctly set up and attached to the system.

##Usage

Execute the script to start collecting weather data. Data collection happens every minute.

```
$ data-stream-processing.py
```

### Data Storage

Data is stored in a QuestDB table named weather_data. The table's schema is:

- **temperature**: Double
- **humidity**: Double
- **pressure**: Double
- **gas_resistance**: Double
- **timestamp**: Timestamp (Partitioned by DAY)