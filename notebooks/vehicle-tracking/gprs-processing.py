import serial
import time
import os
import subprocess

def send_at_command(ser, command, delay=2):
    ser.write((command + '\r\n').encode())
    time.sleep(delay)
    response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
    print(response)
    return response

def set_up_module():
    try:
        # Open the serial port
        ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
        ser.flush()

        # Basic AT command to check if the module responds
        if "OK" not in send_at_command(ser, "AT"):
            print("Failed to communicate with SIM7600 module.")
            return False
        # Reset to factory settings
        send_at_command(ser, "ATZ")
        # Test command
        send_at_command(ser, "AT")


        response = send_at_command(ser, "AT+CREG?")
        if "0,1" not in response and "0,5" not in response:
            print("Module is not registered to the network.")
            return False


        send_at_command(ser, "AT+COPS?")
        

        send_at_command(ser, "AT+CSQ")

        # Set up the PDN context for network registration and RNDIS interface
        send_at_command(ser, "AT+CGDCONT=1,\"IPV4V6\",\"free\"")
        
        send_at_command(ser, "AT+CGDCONT=6,\"IPV4V6\",\"free\"")
            

        ser.close()
        return True

    except Exception as e:
        print(f"Error setting up module: {e}")
        return False

def get_ip_for_usb0():
    try:
        # Activate usb0 interface
        os.system("sudo ifconfig usb0 up")

        # Get IP using DHCP
        result = subprocess.run(['sudo', 'dhclient', 'usb0'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Failed to get IP for usb0 using DHCP.")
            print(result.stderr)
            return False

        return True

    except Exception as e:
        print(f"Error getting IP for usb0: {e}")
        return False

if __name__ == "__main__":
    if set_up_module() and get_ip_for_usb0():
        print("Internet connection established!")
    else:
        print("Failed to establish an internet connection.")
