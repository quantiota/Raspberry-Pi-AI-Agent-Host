import psycopg2
from time import sleep
import serial

# Database Configuration
conn = psycopg2.connect(
    dbname="qdb",
    user="admin",
    password="quest",
    host="docker_host_ip_address",
    port="8812"
)

# Create table if it doesn't exist
with conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS gps_data (latitude DOUBLE, longitude DOUBLE, altitude DOUBLE, speed DOUBLE, timestamp TIMESTAMP) TIMESTAMP(timestamp) PARTITION BY DAY;")

# Serial Configuration
portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"

def parseGPS(data, speed=None):
    if data[0:6] == "$GPGGA":
        sdata = data.split(",")
        time = sdata[1]
        lat = sdata[2]
        dirLat = sdata[3]
        lon = sdata[4]
        dirLon = sdata[5]
        altitude = sdata[9]

        latitude = float(lat[:2]) + float(lat[2:])/60
        if dirLat == 'S':
            latitude = -latitude

        longitude = float(lon[:3]) + float(lon[3:])/60
        if dirLon == 'W':
            longitude = -longitude

        altitude = float(altitude)

        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO gps_data (latitude, longitude, altitude, speed, timestamp) VALUES (%s, %s, %s, %s, NOW());",
                           (latitude, longitude, altitude, speed))

    elif data[0:6] == "$GPRMC":
        sdata = data.split(",")
        speed = float(sdata[7]) * 1.852  # Convert knots to km/h

    return speed

print("Connecting Port..")
try:
    serw = serial.Serial(portwrite, baudrate=115200, timeout=1, rtscts=True, dsrdtr=True)
    
    # Enable GPS
    serw.write('AT+QGPS=1\r'.encode())
    response = serw.readline().decode('utf-8')
    print("Modem Response for AT+QGPS=1:", response.strip())    
    serw.close()
    
except Exception as e: 
    print("Serial port connection failed.")
    print(e)

print("Receiving GPS data\n")
ser = serial.Serial(port, baudrate=115200, timeout=0.5, rtscts=True, dsrdtr=True)
speed = None
while True:
    data = ser.readline().decode('utf-8')
    print("Raw Data:", data)  
    speed = parseGPS(data, speed)
    sleep(1)
