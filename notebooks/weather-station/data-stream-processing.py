#!/usr/bin/env python

import bme680
from datetime import datetime
import time
import psycopg2

print("""indoor-air-quality.py - Estimates indoor air quality.

Runs the sensor for a burn-in period, then uses a
combination of relative humidity and gas resistance
to estimate indoor air quality as a percentage.

Press Ctrl+C to exit!

""")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="qdb",
    user="admin",
    password="quest",
    host="docker_host_ip_address",
    port="8812"
)

# Create the necessary table if it doesn't exist
with conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        temperature DOUBLE,
        humidity DOUBLE,
        pressure DOUBLE,
        gas_resistance DOUBLE,
        iaq DOUBLE,
        timestamp TIMESTAMP
    );
    """)
    cursor.close()

# Initialize the BME680 sensor
# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Configuration for the BME680 sensor
# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Collect burn-in data for gas sensor
# start_time and curr_time ensure that the
# burn_in_time (in seconds) is kept track of.

start_time = time.time()
curr_time = time.time()
burn_in_time = 30
burn_in_data = []

    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.

print('Collecting gas resistance burn-in data for 5 mins\n')

while curr_time - start_time < burn_in_time:
    curr_time = time.time()
    if sensor.get_sensor_data() and sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        burn_in_data.append(gas)
        print('Gas: {0} Ohms'.format(gas))
        time.sleep(1)

gas_baseline = sum(burn_in_data[-50:]) / 50.0

# Set the humidity baseline to 40%, an optimal indoor humidity
hum_baseline = 40.0

  # This sets the balance between humidity and gas reading in the
# calculation of air_quality_score (25:75, humidity:gas)
hum_weighting = 0.25

print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(
        gas_baseline,
        hum_baseline))

# Collect and process data indefinitely
while True:
    if sensor.get_sensor_data() and sensor.data.heat_stable:
        temperature = sensor.data.temperature
        humidity = sensor.data.humidity
        pressure = sensor.data.pressure
        gas_resistance = sensor.data.gas_resistance 
        timestamp = datetime.now()

        
        gas_offset = gas_baseline - gas_resistance
        hum_offset = humidity - hum_baseline

    # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)
        else:
            hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)
    
    # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (gas_resistance / gas_baseline) * (100 - (hum_weighting * 100))
        else:
            gas_score = 100 - (hum_weighting * 100)

        # Calculate air_quality_score.
        iaq = hum_score + gas_score

        # Insert data into the database
        with conn:
            cursor = conn.cursor()
            insert_query = "INSERT INTO weather_data (temperature, humidity, pressure, gas_resistance, iaq, timestamp) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_query, (temperature, humidity, pressure, gas_resistance, iaq, timestamp))

      
        print("Sensor data inserted:", temperature, humidity, pressure, gas_resistance, iaq, timestamp)
        time.sleep(1)  # Wait for 60 seconds before next reading