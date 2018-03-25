#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
from bluepy import btle

# know-how: https://forum.fhem.de/index.php/topic,82249.15.html

# handles for the MI device
temp_hum_handle = int("0x000e", 16)
noti_set_handle = int("0x0010", 16)
battery_handle = int("0x0018", 16)

class TempHumReadingDelegate(btle.DefaultDelegate):
	''' React to temperature readings. '''
	
	def __init__(self):
		btle.DefaultDelegate.__init__(self)
		self.humidity = None
		self.temperature = None

	def handleNotification(self, cHandle, data):
		if (cHandle == temp_hum_handle):
			str = binascii.b2a_hex(data)
			str = str.decode("hex")
			# T=20.6 H=43.8
			self.temperature = str.split("T=", 1)[1].split(" ", 1)[0]
			self.humidity = str.split("H=", 1)[1]
			self.humidity = self.humidity[:-1] #remove non-printable last character

class XiaomiTempHum:
	'''Control Xiaomi Temperature and Humidity sensor.'''

	def __init__(self, bt_device_adr):
		self._battery = None
		self._humidity = None
		self._temperature = None
		
		if ("-" in bt_device_adr):
			self.bt_device_adr = bt_device_adr.replace("-", ":")
		else:
			self.bt_device_adr = bt_device_adr
			
	def read(self):
		device = btle.Peripheral(self.bt_device_adr)
	
		# battery level
		battery_reading = device.readCharacteristic(battery_handle)
		self._battery = str(int(binascii.b2a_hex(battery_reading), 16))
	
		# temp and humidity reading via callback
		callback = TempHumReadingDelegate()
		device.withDelegate(callback)
		device.writeCharacteristic(noti_set_handle, binascii.a2b_hex('0100'))
		if (device.waitForNotifications(10)):
			self._humidity = callback.humidity
			self._temperature = callback.temperature
	
		try:
			device.disconnect()
		except (btle.BTLEException, IOError):
			pass # may happen we don't care
			
	def get_temperature(self):
		return self._temperature
	
	def get_humidity(self):
		return self._humidity
	
	def get_battery(self):
		return self._battery