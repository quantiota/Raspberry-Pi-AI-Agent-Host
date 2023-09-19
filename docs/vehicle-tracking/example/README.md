## Reading GPS Data with Python

### Overview

This script is designed to read GPS data from a Sixfab device via serial communication. The script utilizes two serial ports: one for writing commands (`/dev/ttyUSB2`) and the other for reading data (`/dev/ttyUSB1`). The script decodes and parses the GPRMC NMEA sentence from the GPS module to extract and display various GPS data points including latitude, longitude, speed, date, and more.

### Prerequisites

- Python3
- `serial` library for Python. You can install it using `pip3 install pyserial.`
### Setup & Usage

1. Ensure that the Sixfab device is connected and the serial ports `/dev/ttyUSB1 `and `/dev/ttyUSB2` are accessible.
2. Run the script:

```
python3 gps.py

```

3. The script will send an initialization command to the GPS module via the write port (/dev/ttyUSB2) and then continuously read GPS data from the read port (/dev/ttyUSB1).
4. The output will display raw GPS data as well as parsed data points such as time, latitude, longitude, and more.
### Key Functions

- `parseGPS(data)`: Accepts raw GPS data as input and extracts various data points. If the script receives valid GPRMC data, it parses the latitude, longitude, speed, and other details.

- decode(coord): Converts GPS coordinates from the format DDDMM.MMMMM to DD degrees MM.MMMMM minutes.

### Troubleshooting

If the script is unable to connect to the serial port, ensure that the device is correctly connected and that the specified serial ports are correct.
Ensure that the user has appropriate permissions to access the serial ports. If not, try running the script as root or add the user to the `dialout` group.