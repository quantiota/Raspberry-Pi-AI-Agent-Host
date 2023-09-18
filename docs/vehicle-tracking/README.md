# Quectel EG25/EC25 Mini PCIe 4G/LTE Module HAT Setup with Python

Combined with the Sixfab 3G – 4G/LTE Base HAT for Raspberry Pi, the EG25/EC25 Mini PCIe 4G/LTE Module offers high-speed cellular connectivity and GPS capabilities, making it ideal for IoT and tracking applications.

## Software Prerequisites

Before initiating the QMI, it's essential to verify that the module is appropriately configured. To check and adjust the settings, you can use `minicom`, a terminal-based serial communication program.

First, connect to the module by executing:

```
minicom -D /dev/ttyUSB2
```
Once connected with `minicom`, run the command `AT+QCFG="usbnet"`. Ensure that the returned value is `0`. If it's not, you need to configure it by sending `AT+QCFG="usbnet",0`.

After making this change, it's crucial to reboot the module. Wait for 10 seconds, then use the command `AT+CFUN=1,1` to perform the reboot.

Once done, you can exit `minicom` by pressing `Ctrl` + `A` followed by `X` and then selecting 'Exit from Minicom'.


## Hardware Prerequisites

- Raspberry Pi 4B 8GB
- Sixfab 3G – 4G/LTE Base HAT for Raspberry Pi
- Quectel EG25/EC25 Mini PCIe 4G/LTE Module


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