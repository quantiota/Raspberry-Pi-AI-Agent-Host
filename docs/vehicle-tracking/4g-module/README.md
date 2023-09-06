## SIM7600G-H 4G HAT for Raspberry Pi (LTE Cat-4)

This is a 4G CAT-4/3G/2G network HAT based on the SIMcom SIM7600E-H for the Raspberry Pi which accepts a 1.8V/3V sim card and supports a range of LTE Cat-4 network bands, including phone calls via AT commands and SMS functionality!

Speeds of up to 50Mbps Uplink* and 150Mbps Downlink* are possible on a 4G network via the onboard SIMcom SIM7600E-H module. The HAT supports GNSS positioning via the GPS, Beidou, GLONASS and LBS Base satellite systems and includes an onboard audio jack and audio decoder support making telephone calls.

The HAT includes a USB interface for testing AT commands, obtaining GPS data etc, whilst the onboard CP2102 UART converter allows for serial debugging. UART breakout pins are also included for use with other development boards. LED indicators assist with debugging, showing the operating status.

A MicroSD card slot is included on the board for storing data such as messages and files. Included in the package is the HAT, an LTE antenna, external GPS antenna, two Micro-USB cables and fixings!


### Features

- Standard Raspberry Pi 40-pin GPIO extension header
- Supports dial-up, telephone call, SMS, TCP, UDP, DTMF, HTTP, FTP
- Supports GPS, BeiDou, Glonass and LBS base station positioning
- Onboard USB interface, to test AT Commands and obtain GPS positioning data
- Onboard CP2102 USB to UART converter, for serial debugging
- Breakout UART control pins, to connect with host boards like Arduino
- SIM card slot supports 1.8V/3V SIM cards
- TF card slot for storing data like files, messages etc
- Onboard audio jack and audio decoder for making telephone calls
- 2x LED indicators, easy to monitor the operating status
- Onboard voltage translator, operating voltage can be configured to 3.3V or 5V via jumper
- Baudrate: 300bps ~ 4Mbps (default: 115200bps)
- Autobauding baudrate: 9600bps ~ 115200bps
- Control via AT commands (3GPP TS 27.007, 27.005, and V.25TER command set)
- Supports SIM application toolkit: SAT Class 3, GSM 11.14 Release 99, USAT


### GPS

Before you begin, ensure you have the following:

- **GPS Module**: Make sure your GPS module is connected correctly to your computer or embedded system.

- **Minicom**: Ensure that Minicom is installed on your system. You can usually install it using your system's package manager.

1. **Open Minicom**: Open your terminal and start Minicom with the following command, replacing **/dev/ttyS0** with your GPS module's serial port:

```
minicom -D /dev/ttyUSB0

```

2. Configure Serial Port: In Minicom, press **Ctrl+A**, then **O** to access the configuration menu. Configure the serial port settings:

**Serial Device**: /dev/ttyUSB0 (or your specific serial port)
**Bps/Par/Bits**: 9600 8N1 (baud rate, data bits, parity, stop bits)
Press **Enter** to save your settings.


3. **AT Command Mode**: Type **AT** and press **Enter** to enter AT command mode. The GPS module should respond with **OK**, indicating you are in AT command mode.


4. **Open GPS**: To activate the GPS module, enter the command:

```
AT+CGPS=1

```

5. **Retrieve GPS Information**: To obtain GPS information, enter:

```
AT+CGPSINFO

```
The GPS module will respond with details such as latitude, longitude, altitude, and more.

6. **Close GPS**: After retrieving the desired information, you can close the GPS module to conserve power:

```
AT+CGPS=0
```
7. **Exit Minicom**: To exit Minicom, press Ctrl+A, then X. Confirm that you want to exit.




### GPRS

The script gprs.conf is a bash script that automates the setup of a GPRS internet connection using the PPP (Point-to-Point Protocol) for cellular communication. The script performs the following tasks:

Checks if **pppd** (PPP daemon) is installed. If not, it installs **ppp**.
Writes a configuration file named **gprs** under **/etc/ppp/peers** for the PPP connection.
Creates a systemd service named **gprs.service** for managing the PPP connection.
Creates an IP-up script named **addroute** under **/etc/ppp/ip-up.d** to add a default route via **ppp0**.


Here's a brief breakdown of what each part of the script does:

- **Installation Check**:
Checks if **pppd** is already installed. If not, it installs it.

- **Peer Configuration**:
Writes the configuration settings for the PPP connection into the **gprs** file under **/etc/ppp/peers**. This file defines various connection parameters such as the serial port, connection speed, and authentication.

- **Systemd Service**:
Creates a systemd service named **gprs.service** under **/etc/systemd/system**. This service is responsible for starting the PPP connection using the configuration defined earlier.

- **IP-Up Script**:
Creates an IP-up script named **addroute** under **/etc/ppp/ip-up.d**. This script runs after the PPP connection is established and adds a default route via the **ppp0** interface.

The script includes error checks to ensure that each step completes successfully. It uses colored output to indicate the status of each task, such as whether it's installing packages, creating files, or setting permissions.

To use this script, you should execute it with root privileges. You can run it using the following command (assuming the script is saved in a file named **gprs-conf.sh**):

``````
sudo su
cat ./gprs-conf.sh | sudo bash

``````

Please make sure to review the script and ensure that it matches your system's configuration and requirements before running it. Remember to replace <**apn**> with the actual provider apn.


After running the script, the GPRS internet connection should be automatically set up and initiated as a systemd service. Here's how you can check and manage the connection:

**Check Status of GPRS Service**:
You can check the status of the GPRS service to see if it's active and running as expected. Open a terminal and use the following command:

``````
systemctl status gprs.service
``````
This will display information about the status of the service, including whether it's active and any recent logs.

**Start the GPRS Service**:
If the GPRS service is not already running, you can start it using the following command:

``````
sudo systemctl start gprs.service
``````
**Stop the GPRS Service**:
To stop the GPRS service, you can use the following command:

``````
sudo systemctl stop gprs.service
``````
**Enable the GPRS Service at Boot**:
If you want the GPRS service to start automatically when the system boots, you can enable it with the following command:

``````
sudo systemctl enable gprs.service
``````
This ensures that the service is started during system startup.

**Disable the GPRS Service at Boot**:
If you no longer want the GPRS service to start automatically at boot, you can disable it with the following command:

``````
sudo systemctl disable gprs.service
``````

**Check IP Address and Test Connectivity**:
After the GPRS service is running, you can check if you have obtained an IP address and test internet connectivity. You can do this using the ifconfig command to check if the ppp0 interface has an IP address, and then use the ping command to test connectivity to a website:

``````
ifconfig ppp0
sudo ping -I ppp0 www.example.com
``````
Replace www.example.com with an actual website URL.

Please note that the behavior of the GPRS connection may vary based on your specific cellular modem and network setup. The provided script sets up a PPP connection, and if everything goes smoothly, you should be able to access the internet through the ppp0 interface. If you encounter any issues, it's a good idea to check the logs and consult the documentation for your cellular modem to troubleshoot further.