
#  Simulated GPS Tracking Data Collection Script

# This script simulates a vehicle path using 
# GPS coordinates and stores the data in a QuestDB database 
# using psycopg2. The script also uses the OpenRouteService API 
# to calculate directions between two points and decodes the 
# resulting geometry into a set of coordinates. The comments 
# added above each section provide explanations for what 
#t he code does in each step.


# Import necessary libraries
from datetime import datetime, timedelta
import time
import psycopg2
import openrouteservice as ors

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
    cursor.execute("CREATE TABLE IF NOT EXISTS gps_data_sample (latitude DOUBLE, longitude DOUBLE, timestamp TIMESTAMP) TIMESTAMP(timestamp) PARTITION BY DAY;")


# Initialize the OpenRouteService client with an API key
client = ors.Client(key='YOUR_OPENROUTESERVICES_KEY')

# Define the start and end coordinates for the simulated vehicle path
start_latitude = 45.208180
start_longitude = 5.760760
end_latitude = 45.209860
end_longitude = 5.783540

# Get directions from start to end coordinates
directions = client.directions(
    coordinates=[(start_longitude, start_latitude), (end_longitude, end_latitude)],
    profile='driving-car',
)

# Extract the geometry of the route and decode it into coordinates
geometry = directions['routes'][0]['geometry']
coordinates = ors.convert.decode_polyline(geometry, is3d=False)

# Get the current timestamp
current_time = datetime.now()

# Insert the coordinates into the database with timestamps
with conn:
    cursor = conn.cursor()
    for coordinate in coordinates['coordinates']:
        longitude, latitude = coordinate  # Unpack the coordinate values

        # Insert data into the gps_data table
        cursor.execute(
            "INSERT INTO gps_data_sample (latitude, longitude, timestamp) VALUES (%s, %s, %s);",
            (latitude, longitude, current_time)
        )

       # Increment current time for the next coordinate
        current_time += timedelta(seconds=30)