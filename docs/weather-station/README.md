## BME680 Sensor Setup with Python

The BME680 is an integrated environmental sensor developed specifically for mobile applications and wearables. It combines individual high linearity, high accuracy sensors for pressure, humidity, temperature, and volatile organic compounds (VOCs).

### Hardware Prerequisites

- Raspberry Pi or a similar device.
- BME680 sensor.
- Breadboard and jumper wires (optional but useful for prototyping).


## Software Setup

1. I2C: enables support for I2C based hardware:

With root:dietpi login credentials:

Run dietpi-software from the command line.

```
dietpi-software
```
Choose Browse Software and select I2C. Finally select Install. DietPi will do all the necessary steps to install and start the software item.


```
 [*] 72  I2C: enables support for I2C based hardware

```

2. Reboot:

```
sudo shutdown -r now

```

3. Install the Python library for the BME680 sensor:

```
sudo pip3 install bme680

```


## Hardware Connection

1. Connect the BME680 sensor to your Raspberry Pi using the I2C interface. Here's a basic connection guide:

- **VCC** of BME680 to **3.3V** of Raspberry Pi
- **GND** of BME680 to **GND** of Raspberry Pi
- **SDA** of BME680 to **SDA** (GPIO2) of Raspberry Pi
- **SCL** of BME680 to **SCL** (GPIO3) of Raspberry Pi

2. (Optional) Use i2cdetect to ensure that the device is correctly connected:

```
sudo i2cdetect -y 1

```

This command should display a matrix, and one of the addresses should be 0x76 or 0x77, which represents the BME680 sensor.

## Python Usage

Here's a simple Python script to read data from the BME680 sensor:

```
import bme680

sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print("Temperature:", sensor.data.temperature)
print("Pressure:", sensor.data.pressure)
print("Humidity:", sensor.data.humidity)
print("Gas resistance:", sensor.data.gas_resistance)

```

Save this script, run it with Python, and it will display readings from your BME680 sensor.