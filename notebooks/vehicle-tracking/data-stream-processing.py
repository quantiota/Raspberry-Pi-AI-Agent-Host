
from datetime import datetime, timedelta
#!/usr/bin/python3
# -*- coding:utf-8 -*-

import psycopg2
import serial
import time

# Connect to the QuestDB database
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
    cursor.execute("CREATE TABLE IF NOT EXISTS gps_data (latitude DOUBLE, longitude DOUBLE, altitude DOUBLE, speed DOUBLE, timestamp TIMESTAMP) TIMESTAMP(timestamp) PARTITION BY DAY;")



ser = serial.Serial('/dev/ttyS0', 115200)
ser.flushInput()

def send_at(command, back, timeout):
    rec_buff = ''
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting()).decode()
    return rec_buff

def get_gps_position():
    rec_null = True
    answer = ''
    print('Start GPS session...')
    send_at('AT+CGPS=1,1', 'OK', 1)
    time.sleep(2)
    
    while True:
        answer = send_at('AT+CGPSINFO', '+CGPSINFO: ', 1)
        if '+CGPSINFO:' in answer:
            gps_info_str = answer.split(":")[1].strip()
            gps_info_list = gps_info_str.split(",")

            latitude = gps_info_list[0]
            latitude_direction = gps_info_list[1]
            longitude = gps_info_list[2]
            longitude_direction = gps_info_list[3]

            latitude_degree = float(latitude[:2])
            latitude_minute = float(latitude[2:])
            latitude = latitude_degree + latitude_minute / 60.0

            longitude_degree = float(longitude[:3])
            longitude_minute = float(longitude[3:])
            longitude = longitude_degree + longitude_minute / 60.0

            date = gps_info_list[4]
            time_utc = float(gps_info_list[5])
            altitude = float(gps_info_list[6])
            speed = float(gps_info_list[7])

            print(f"Latitude: {latitude} {latitude_direction}")
            print(f"Longitude: {longitude} {longitude_direction}")
            print(f"Date: {date}")
            print(f"Time: {time_utc}")
            print(f"Altitude: {altitude} m")
            print(f"Speed: {speed} knots")

            # Insert data into the QuestDB table
            with conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO gps_data (latitude, longitude, altitude, speed, timestamp) VALUES (%s, %s, %s, %s, NOW());",
                               (latitude, longitude, altitude, speed))


        else:
            print('GPS is not ready')

        time.sleep(1.5)

try:
    get_gps_position()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if ser is not None:
        ser.close()
    if conn is not None:
        conn.close()

