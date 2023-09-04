#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6
rec_buff = ''
APN = 'CMNET'
ServerIP = '118.190.93.84'
Port = '2317'
Message = 'Waveshare'

def power_on(power_key):
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(20)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down(power_key):
	print('SIM7600X is loging off:')
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(18)
	print('Good bye')
	
def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.1 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			print(command + ' ERROR')
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
			print(rec_buff.decode())
			return 1
	else:
		print(command + ' no responce')

try:
	power_on(power_key)
	send_at('AT+CSQ','OK',1)
	send_at('AT+CREG?','+CREG: 0,1',1)
	send_at('AT+CPSI?','OK',1)
	send_at('AT+CGREG?','+CGREG: 0,1',0.5)
	send_at('AT+CGSOCKCONT=1,\"IP\",\"'+APN+'\"','OK',1)
	send_at('AT+CSOCKSETPN=1', 'OK', 1)
	send_at('AT+CIPMODE=0', 'OK', 1)
	send_at('AT+NETOPEN', '+NETOPEN: 0',5)
	send_at('AT+IPADDR', '+IPADDR:', 1)
	send_at('AT+CIPOPEN=0,\"TCP\",\"'+ServerIP+'\",'+Port,'+CIPOPEN: 0,0', 5)
	send_at('AT+CIPSEND=0,', '>', 2)#If not sure the message number,write the command like this: AT+CIPSEND=0, (end with 1A(hex))
	ser.write(Message.encode())
	if 1 == send_at(b'\x1a'.decode(),'OK',5):
		print('send message successfully!')
	send_at('AT+CIPCLOSE=0','+CIPCLOSE: 0,0',15)
	send_at('AT+NETCLOSE', '+NETCLOSE: 0', 1)
	power_down(power_key)
except:
	if ser != None:
		ser.close()
		GPIO.cleanup()

if ser != None:
		ser.close()
		GPIO.cleanup()