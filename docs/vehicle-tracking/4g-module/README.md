# Sixfab 4G/LTE Cellular Modem Kit for Raspberry Pi

### Overview

The Sixfab Base HAT is specifically designed for Raspberry Pi, serving as a pre-certified carrier board to ensure seamless integration. To further simplify the process, the Sixfab CORE middleware automatically installs and configures all necessary settings on both the OS and the LTE modem. This feature-rich middleware also provides a remote terminal, making configuration and support straightforward. For those diving into IoT projects, the kit comes with an IoT SIM, offering options for either global or regional coverage. 


### Key Features & Benefits

- **Tailored for Raspberry Pi**: Designed exclusively for Raspberry Pi, the kit offers seamless cellular integration.

- **Certified Connectivity**: Utilize the pre-certified Sixfab Base HAT for reliable carrier board support.

- **Effortless Configuration**: Sixfab CORE software automates OS and LTE modem setup for simplicity.

- **Remote Management**: Access remote terminal, configuration, and support for network control.

- **Sixfab IoT SIM**: Choose global or regional data plans to suit your project’s needs (pricing details).

- **Cost-Efficient Start**: The kit includes a $25 data credit coupon code; no commitment is required.

- **All-in-One Kit**: With antennas, cables, headers, and spacers, it’s ready to connect right out of the box!


# QMI Mode Cellular Connection Setup for Raspberry Pi (as `wwan0`)

This guide explains how to set up a cellular connection on your Raspberry Pi using QMI mode, which exposes a `wwan0` interface.

## Prerequisites

- Raspberry Pi with a Quectel modem or similar, which should preferably be in QMI mode.
- `libqmi-utils` and `udhcpc` packages installed.
- APN (Access Point Name) for your cellular network provider.

## Installation

1. Install the required utilities:

   ```
   sudo apt update && sudo apt install libqmi-utils udhcpc
   ```
   

## Configuration

1. Verify the modem's operating mode:

```
sudo qmicli -d /dev/cdc-wdm0 --dms-get-operating-mode

```
- If not in 'online' mode, set it:

```
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='online'

```

2. Set the interface to raw_ip mode:

```
sudo ip link set wwan0 down
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up

```

3. Connect to the cellular network using the provided APN USERNAME and PASSWORD:


```
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='YOUR_APN',username='YOUR_USERNAME',password='YOUR_PASSWORD',ip-type=4" --client-no-release-cid


```

4. Obtain an IP address and set up routing

```
sudo udhcpc -q -f -i wwan0

```

Test the connection with:

```
ping -I wwan0 www.google.com -c 5
```