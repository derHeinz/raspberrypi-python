#!/usr/bin/python
# -*- coding: utf-8 -*-

import pexpect # install with: pip install pexpect
import argparse
import datetime
import imp
import time
import binascii
import urllib2
import threading
import postopenhab
from bluepy import btle

# location of bluepy
#bluepy_location = '/home/pi/bluepy/bluepy/btle.py'
# load bluepy
#btle = imp.load_source('btle', bluepy_location)

bt_rad_message_type = "bt_rad"


class BluetoothCommand:
	"""Creates bluetooth functionality to work wit radiator"""
	def __init__(self, bt_device_adr):
		if ("-" in bt_device_adr):
			self.bt_device_adr = bt_device_adr.replace("-", ":")
		else:
			self.bt_device_adr = bt_device_adr
			
	def get_temp(self):
		self._connect()
		values = self._get_info()
		temp = int(values.split()[5], 16) / 2.0
		self._disconnect()
		return temp

	def get_vent(self):
		self._connect()
		values = self._get_info()
		vent = int(values.split()[3], 16)
		self._disconnect()
		return vent

	def get_mode(self):
		self._connect()
		values = self._get_info()
		mode = values.split()[2]
		modestr = 'Unbekannt'
		if mode == '08':
			modestr = 'Automatik'
		if mode == '09':
			modestr = 'Manuell'
		if mode == '0a':
			modestr = 'Urlaub'
		if mode == '0c':
			modestr = 'Boost'
		if mode == '18':
			modestr = 'Fenster auf'
		if mode == '28':
			modestr = 'Locked'
		self._disconnect()
		return modestr	
		
	def set_daytime(self, daytime):
		self._connect()
		val = '43'
		if daytime == 'ON':
			val = '43'
		if daytime == 'OFF':
			val = '44'
		# send data
		self._set_value(val)
		self._disconnect()
		return "OK"
	
	def set_temp(self, temp):
		self._connect()
		val = float(temp)
		val = int(val / 0.5)
		temp_hex = hex(val)[2:]
		# write to handle
		self._set_value('41' + temp_hex)
		self._disconnect()
		return 'OK'

	def set_boost(self, on_or_off):
		self._connect()
		if (on_or_off):
			value = '4501'
		else:
			value = '4500'
		self._set_value('41' + value)
		self._disconnect()
		return 'OK'
		
	def set_time(self):
		self._connect()
		datetimeobj = datetime.datetime.now()
		command_prefix = "03"
		year = "{:02X}".format(datetimeobj.year % 100)
		month = "{:02X}".format(datetimeobj.month)
		day = "{:02X}".format(datetimeobj.day)
		hour = "{:02X}".format(datetimeobj.hour)
		minute = "{:02X}".format(datetimeobj.minute)
		second = "{:02X}".format(datetimeobj.second)
		control_string = "{}{}{}{}{}{}{}".format(command_prefix, year, month, day, hour, minute, second)
		self._set_value(control_string)
		self._disconnect()

class PExpectBC(BluetoothCommand):
	"""Uses the Pexpect library to communicate with bluetooth"""
	def _connect(self):
		self.gatt = pexpect.spawn('gatttool -b ' + self.bt_device_adr + ' --interactive')
		self.gatt.expect('\[LE\]>')
		self.gatt.sendline('connect')
		self.gatt.expect('\[CON\]')

	def _disconnect(self):
		self.gatt.sendline('disconnect')
		self.gatt.sendline('quit')

	def _get_info(self):
		# write to the handle
		self.gatt.sendline('char-write-req 0x0411 03')
		# get back notifications
		self.gatt.expect('Notification handle = .*')
		values = self.gatt.after.split('\n')[0].split(': ')[1]
		return values
	
	def _set_value(self, hex_value):
		self.gatt.sendline('char-write-req 0x0411 ' + hex_value)
		self.gatt.expect('Characteristic value was written successfully')

class ReceiveInfoDelegate(btle.DefaultDelegate):
	def __init__(self):
		btle.DefaultDelegate.__init__(self)
		self.data = ""

	def handleNotification(self, cHandle, data):
		if (cHandle == radiator_noti_handle):
			self.data = binascii.b2a_hex(data)
		else:
			postopenhab.post_systemnotification("Heizthermostat-Fehler. Receive Error.", bt_rad_message_type)

radiator_handle = int("0x0411", 16)
radiator_noti_handle = int("0x0421", 16)
			
class BluepyBC(BluetoothCommand):
	"""Uses Bluepy to communicate with bluetooth"""
	def _connect(self):
		self.device = btle.Peripheral(self.bt_device_adr)

	def _disconnect(self):
		self.device.disconnect()

	def _get_info(self):
		# write to the handle and wait for notification
		delegate = ReceiveInfoDelegate()
		self.device.setDelegate(delegate)
		th = threading.Thread(target=self._thread_receiveNotification)
		th.start()
		self.device.writeCharacteristic(radiator_handle, binascii.a2b_hex('03'), True)
		th.join()
		# instead of '02 01 09 00 04 0a' we get '02010900040a' from delegate.data -> reformat
		
		result = ""
		count = -1
		for i in delegate.data:
			count += 1
			if count>0 and count%2==0:
				result += " "
			result += i

		return result
		
	def _set_value(self, hex_value):
		self.device.writeCharacteristic(radiator_handle, binascii.a2b_hex(hex_value), True)
		
	def _thread_receiveNotification(self):
		self.device.waitForNotifications(10.0) # should normally return within this time

def main():
	parser = argparse.ArgumentParser(description="Control eq-3 Bluetooth Heater.")
	parser.add_argument("-a", dest = "address", metavar = "address", nargs = "?",
		help="MAC Address of the BT device.")
	parser.add_argument("-c", dest = "command", metavar = "command", nargs = "?",
		help="Options: getTemp, setTemp, getVent, setVent, getMode, setMode, setBoost, setDay, setTime.")
	parser.add_argument("-v", dest = "value", metavar = "value", nargs = "?",
		help="Optional value if a set function is used that needs it.")
	args = parser.parse_args()
	bt_cmd = BluepyBC(args.address)
	try:
		if (args.command == 'getTemp'):
			what = "Temperatur auslesen."
			result = bt_cmd.get_temp()
		elif (args.command == 'getVent'):
			what  = "Ventilstand auslesen."
			result = bt_cmd.get_vent()
		elif (args.command == 'getMode'):
			what = "Modus auslesen."
			result = bt_cmd.get_mode()
		elif (args.command == 'setTime'):
			what = "Aktuelle Zeit setzen."
			result = bt_cmd.set_time()
		elif (args.command == 'setTemp'):
			what = "Temperatur setzen."
			result = bt_cmd.set_temp(args.value)
		elif (args.command == 'setDay'):
			what = "Tag/Nacht Modus setzen."
			result = bt_cmd.set_daytime(args.value)
		elif (args.command == 'setBoost'):
			what = "Boost setzen."
			result = bt_comd.set_boost(args.value)
		else:
			result = "Error: no command"
	except btle.BTLEException as e:
		# temporary commented due to BT problems with eq3
		# postopenhab.post_systemnotification("Heizthermostat-Fehler beim " + what , bt_rad_message_type)
		print e
		
		print "Error: Keine Kommunikation zu Thermostat."
	else:
		print result

if __name__ == "__main__":
	main()
