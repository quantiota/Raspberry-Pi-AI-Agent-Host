
# Raspberry Pi 4 Case for Teltonika Calxy Module


![Raspberry Pi Case](https://raw.githubusercontent.com/quantiota/Raspberry-Pi-AI-Agent-Host/refs/heads/main/docs/edge-connectivity/stl/0857_EBD050AM00_01.png)




## 3D Printing Service

[sculpteo](https://www.sculpteo.com/en/services/online-3d-printing-service/)




![Raspberry Pi Case](https://raw.githubusercontent.com/quantiota/Raspberry-Pi-AI-Agent-Host/refs/heads/main/docs/edge-connectivity/stl/0857_EBD050AM00_02.png)



![Raspberry Pi Case](https://raw.githubusercontent.com/quantiota/Raspberry-Pi-AI-Agent-Host/refs/heads/main/docs/edge-connectivity/stl/0857_EBD050AM00_03.png)




## Cellular modem (Calyx HAT)

Install the only required package (`modprobe`):

```bash
sudo apt update
sudo apt install kmod
```

Load the driver and bind the Teltonika USB ID:

```bash
sudo modprobe usbserial
sudo modprobe option
echo "1d12 0101" | sudo tee /sys/bus/usb-serial/drivers/option1/new_id
```

Persist across reboots (systemd oneshot):

```bash
sudo tee /etc/systemd/system/calyx-modem.service >/dev/null <<'EOF'
[Unit]
Description=Load Calyx cellular modem driver binding
After=multi-user.target
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/sbin/modprobe usbserial
ExecStart=/sbin/modprobe option
ExecStart=/bin/sh -c 'echo "1d12 0101" > /sys/bus/usb-serial/drivers/option1/new_id'
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now calyx-modem.service
```

## APN (Free Mobile, France = `free`)

```bash
sudo apt install microcom
sudo microcom -p /dev/ttyUSB2
```

In microcom (no local echo — type `ATE1` + Enter to see your input):

```
ATE1
AT+CPIN?
AT+CGDCONT=1,"IP","free"
```
