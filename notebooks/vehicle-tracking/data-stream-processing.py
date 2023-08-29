
from datetime import datetime, timedelta
import time
import psycopg2

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


# data collection
















# Insert data into the gps_data table

    cursor.execute(
            "INSERT INTO gps_data (latitude, longitude, timestamp) VALUES (%s, %s, %s);",
            (latitude, longitude, timestamp)
        )

