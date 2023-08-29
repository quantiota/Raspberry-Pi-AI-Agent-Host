
from datetime import datetime, timedelta
import time
import psycopg2
import openrouteservice as ors

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
    cursor.execute("CREATE TABLE IF NOT EXISTS gps_data (latitude DOUBLE, longitude DOUBLE, timestamp TIMESTAMP) TIMESTAMP(timestamp) PARTITION BY DAY;")


# Simulate a vehicle path
client = ors.Client(key='YOUR_OPENROUTESERVICES_KEY')

# Enter a start and end address location
start_latitude = 45.208180
start_longitude = 5.760760
end_latitude = 45.209860
end_longitude = 5.783540

directions = client.directions(
    coordinates=[(start_longitude, start_latitude), (end_longitude, end_latitude)],
    profile='driving-car',
)

geometry = directions['routes'][0]['geometry']
coordinates = ors.convert.decode_polyline(geometry, is3d=False)

current_time = datetime.now()

with conn:
    cursor = conn.cursor()
    for coordinate in coordinates['coordinates']:
        longitude, latitude = coordinate  # Unpack the coordinate values

        # Insert data into the gps_data table
        cursor.execute(
            "INSERT INTO gps_data (latitude, longitude, timestamp) VALUES (%s, %s, %s);",
            (latitude, longitude, current_time)
        )

        # Increment current time
        current_time += timedelta(seconds=30)