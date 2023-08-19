#!/usr/bin/env python


import bme680
from datetime import datetime
import time
import psycopg2


# Connect without specifying the isolation_level
conn = psycopg2.connect(
    dbname="qdb",
    user="admin",
    password="quest",
    host="docker_host_ip_address",
    port="8812"
)



with conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE  IF NOT EXISTS weather_data (temperature DOUBLE, humidity DOUBLE, pressure DOUBLE, gas_resistance DOUBLE, timestamp TIMESTAMP) TIMESTAMP(timestamp) PARTITION BY DAY;")

# Try to create an instance of the BME680 sensor using its primary I2C address.
# If unsuccessful, fall back to its secondary address.

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Print the calibration data for the sensor. This is used internally to give accurate readings.
# These calibration data can safely be commented out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):
    if not name.startswith('_'):  # Ignore private attributes
        value = getattr(sensor.calibration_data, name)
        if isinstance(value, int):  # Only print integer values
            print('{}: {}'.format(name, value))

# Set the gas heater temperature and duration for the gas sensor. This ensures accurate readings.

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Note: Additional heater profiles can be set if needed. Here's an example for reference:
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)


while True:
    if sensor.get_sensor_data():
        temperature = sensor.data.temperature
        humidity = sensor.data.humidity
        pressure = sensor.data.pressure
        gas_resistance = sensor.data.gas_resistance 
        timestamp = datetime.now()

        with conn:
            cursor = conn.cursor()

            # Insert sensor data into the table
            insert_query = "INSERT INTO weather_data (temperature, humidity, pressure, gas_resistance, timestamp) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(insert_query, (temperature, humidity, pressure, gas_resistance, timestamp))

        print("Sensor data inserted:", temperature, humidity, pressure, gas_resistance, timestamp)

    # Wait for a while before taking the next reading
    time.sleep(60)  # Wait for 60 second