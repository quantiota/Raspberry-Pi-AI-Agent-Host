## SIM7600E-H 4G HAT GPS Tracker

### Overview

This script is designed to interact with the SIM7600E-H 4G HAT GPS module to retrieve GPS location data and store it in a QuestDB database. It establishes a connection to the database, creates a table if it doesn't exist, and sets up the serial communication with the GPS module. The script continuously queries the GPS module for its information using AT commands and extracts relevant GPS parameters such as latitude, longitude, altitude, speed, and timestamp. These parameters are then transformed and formatted for better readability. The latitude and longitude values are calculated from degree and minute components and stored in the database along with other extracted information. Any errors encountered during the process are gracefully handled, and the serial port and database connection are properly closed at the end. The script offers an efficient and reliable way to capture and manage GPS data from the SIM7600E-H 4G HAT GPS module

###  Set up parameter:

After installing the AI Agent Host, open VS Code in your browser through an HTTPS connection. Navigate to >project/vehicle-tracking/data-stream-processing.py.
The script is pre-configured to connect to a QuestDB instance using the following credentials:

```
dbname="qdb",
user="admin",
password="quest",
host="yourhost.freeddns.org",
port="8812"
```

Remember to replace **<yourhost.freeddns.org>** with the actual DDNS domain name that points to the IP address of the Docker host where your Raspberry Pi is running.

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



### Run Python File in Terminal:
Execute the Python script from the terminal to start collecting gps data data.


### Connect to Grafana Dashboard:
Open your browser and navigate to the Grafana interface. Select the GPS Tracker dashboard to start monitoring your data in real-time



![GPS Tracker Dashboard](./gps_tracker_dashboard.png)


### Customizing the GPS Tracker:

While the pre-configured GPS tracker setup is designed to work out of the box, you can also customize it to match your unique requirements. Here are some steps to consider when customizing the setup:

- **Modify Data Stream Processing**: The Python script responsible for processing GPS data can be customized to include additional data points or calculations. For example, you could include data related to vehicle speed, direction, or any other sensor readings.

- **Enhance Grafana Dashboard**: The Grafana dashboard can be tailored to display the additional data points collected from the GPS tracker. You can add new panels, visualizations, and filters to create a dashboard that provides valuable insights for your specific use case.

- **Integrate with External Services**: If you have specific external services or APIs you'd like to integrate with, you can modify the Python script to send data to those services. This could include data storage in cloud platforms, real-time alerts, or other notifications.

- **Fine-Tune GPS Accuracy**: Depending on your tracking needs, you can explore ways to improve GPS accuracy, such as fine-tuning the frequency of data collection, incorporating more advanced GPS modules, or implementing data filtering algorithms.

- **Advanced Analytics**: If you're looking to extract advanced insights from the collected GPS data, you can incorporate data analysis techniques, machine learning models, or predictive analytics to derive valuable information from the tracker's data stream.