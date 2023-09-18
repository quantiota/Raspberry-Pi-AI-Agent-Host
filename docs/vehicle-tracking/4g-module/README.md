# Sixfab 3G – 4G/LTE Base HAT for Raspberry Pi with EG25-G Mini PCIe

### Overview

The Quectel EG25-G Mini PCIe is an LTE Category 4 module designed in the standard PCI Express® Mini Card form factor. Tailored for M2M and IoT applications, it boasts data rates of up to 150Mbps for download and 50Mbps for upload. Notably, it ensures connectivity in areas lacking 4G or 3G as it's also compatible with EDGE and GSM/GPRS networks. The module incorporates Qualcomm® IZat™ Gen8C Lite location technology, supporting multiple satellite systems like GPS, GLONASS, BeiDou/Compass, Galileo, and QZSS, ensuring swift and precise positioning. Furthermore, its extensive set of Internet protocols, industry-standard interfaces, and diverse functionalities make it suitable for various M2M applications, including industrial routers, PDAs, rugged tablets, and digital signage. 


### Key Benefits

- LTE category 4 module optimized for broadband IoT
applications
- Worldwide LTE, UMTS/HSPA+ and GSM/GPRS/EDGE coverage
- Standard PCI Express® Mini Card form factor (Mini PCIe) ideal
- for manufacturers to easily integrate wireless connectivity
into their devices
- MIMO technology meets demands for data rate and link
reliability in modem wireless communication systems
- Multi-constellation GNSS receiver available for applications
requiring fast and accurate fixes in any environment


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

3. Connect to the cellular network using the provided APN, USERNAME and PASSWORD:


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


## Reconnection after Reboot

After a system reboot, you'll need to rerun the following to reconnect:


```

sudo ip link set wwan0 down
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='YOUR_APN',username='YOUR_USERNAME',password='YOUR_PASSWORD',ip-type=4" --client-no-release-cid
sudo udhcpc -q -f -i wwan0
```


## Automate Reconnection

To automatically reconnect on system boot, create a configuration file:

```
sudo nano /etc/network/interfaces.d/wwan0

```

Add the following content (replace 'YOUR_APN' with your APN, USERNAME and PASSWORD):

```
auto wwan0
iface wwan0 inet manual
     pre-up ifconfig wwan0 down
     pre-up echo Y > /sys/class/net/wwan0/qmi/raw_ip
     pre-up for _ in $(seq 1 10); do /usr/bin/test -c /dev/cdc-wdm0 && break; /bin/sleep 1; done
     pre-up for _ in $(seq 1 10); do /usr/bin/qmicli -d /dev/cdc-wdm0 --nas-get-signal-strength && break; /bin/sleep 1; done
     pre-up sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='YOUR_APN',username='YOUR_USERNAME',password='YOUR_PASSWORD',ip-type=4" --client-no-release-cid
     pre-up udhcpc -i wwan0
     post-down /usr/bin/qmi-network /dev/cdc-wdm0 stop

```

Now, after rebooting, wwan0 should come up automatically without manual intervention.