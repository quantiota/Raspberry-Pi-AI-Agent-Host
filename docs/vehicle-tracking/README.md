## SIM7600G-H 4G HAT Setup with Python

The SIM7600G-H is a compact 4G HAT module designed for Raspberry Pi. It offers high-speed cellular connectivity and GPS capabilities, making it ideal for IoT and tracking applications.

### Hardware Prerequisites

- Raspberry Pi.
- SIM7600G-H HAT


## Software Setup

1. UART: enables support for UART based hardware:

With root:dietpi login credentials:

Run dietpi-software from the command line.

```
dietpi-software
```
Browse DietPi-Config > Advanced Options > Serial/UART. Choose ttyS0. Finally select OK. DietPi will do all the necessary steps to install and start the software item.


```
   ttyS0 (mini UART) device : [On] 

```

2. Reboot:

```
sudo shutdown -r now

```


## Hardware Connection

1. Begin by connecting the SIM7600G-H HAT to your Raspberry Pi using the GPIO interface with the default jumper setting. 

2. (Optional) To ensure proper device connectivity, you can use minicom. If not installed, you can install it using the following command:


```
sudo apt install minicom -y

```

Set up the connection using:

```
sudo minicom -s

```

Establish the connection:


```
sudo minicom -D /dev/ttyS0

```

Setting Up the SIM:


```
AT+CPIN?                # Verify if the SIM card PIN is enabled
 +CPIN: SIM PIN

AT+CLCK="SC",0,"<PIN>"  # Disable the PIN using your default PIN code, e.g., AT+CLCK="SC",0,"1234"
 OK

AT+CPIN?                #verify:
 +CPIN: READY

```


3. Serial Port Configuration

So, for your Docker Compose configuration:

devices:
  - "/dev/tty0:/dev/tty0"


Remember, the important part is identifying which port your 4g Module is connected to and then configuring your software or Docker container to use that specific port.

