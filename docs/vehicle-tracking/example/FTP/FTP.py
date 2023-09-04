#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial("/dev/ttyS0",115200)
ser.flushInput()

power_key = 6
rec_buff = ''
ftp_user_name = 'user'
ftp_user_password = 'waveshare'
ftp_server = '113.81.235.52'
download_file_name = 'index.htm'
upload_file_name = 'index.htm'

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

def configureFTP(server,u_name,u_password):
	send_at('AT+CFTPPORT=21','OK',1)
	send_at('AT+CFTPMODE=1','OK',1)
	send_at('AT+CFTPTYPE=A','OK',1)
	send_at('AT+CFTPSERV='+'\"'+server+'\"','OK',1)
	send_at('AT+CFTPUN='+'\"'+u_name+'\"','OK',1)
	send_at('AT+CFTPPW='+'\"'+u_password+'\"','OK',1)

def downloadFromFTP(file_name):
	print('Download file from FTP...')
	send_at('AT+CFTPGETFILE='+'\"'+file_name+'\",0','OK',1)

def uploadToFTP(file_name):
	print('Download file from FTP...')
	send_at('AT+CFTPGETFILE='+'\"'+file_name+'\",0','OK',1)

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

try:
	power_on(power_key)
	configureFTP(ftp_server,ftp_user_name,ftp_user_password)
	time.sleep(0.5)
	print('Downloading file form \"'+ftp_server+'\"...')
	downloadFromFTP(download_file_name)
	time.sleep(1)
	print('Uploading file to \"'+ftp_server+'\"...')
	uploadToFTP(upload_file_name)
	power_down(power_key)
except :
	if ser != None:
		ser.close()
	GPIO.cleanup()