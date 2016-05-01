#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp #make imports during runtime
import time
import binascii
import postopenhab #own lib in directory
import argparse #used for parsing command line arguments
import rpyc #install with sudo pip install rpyc
import socket
import sys
import threading

# location of bluepy
bluepy_location = '/home/pi/bluepy/bluepy/btle.py'
# load bluebpy
btle = imp.load_source('btle', bluepy_location)
# message type in openhab
bt_havir_message_type = "bt_hav"
# port for the server to serve remote BT requests
bt_havir_port = 18861

# handles for the HAVIR device
beep_handle = int("0x000e", 16)
noti_set_handle = int("0x0016", 16)
noti_recv_handle = int("0x0014", 16)

class Antilost:
	def __init__(self, bt_device_adr):
		if ("-" in bt_device_adr):
			self.bt_device_adr = bt_device_adr.replace("-", ":")
		else:
			self.bt_device_adr = bt_device_adr

class RemoteAntilost(Antilost):
	''' Does remotely access a server and call functions on em. '''
	
	def __init__(self, bt_device_adr):
		Antilost.__init__(self, bt_device_adr)
		self._connected = False

	def connect(self):
		if not self._connected:
			try:
				self.connection = rpyc.connect("localhost", bt_havir_port)
				self._connected = True
				return True
			except socket.error:
				#print("Exception")
				return False
	
	def disconnect(self):
		self.connection.disconnect()

	def beep(self):
		self.connection.root.exposed_beep()
	
	def unbeep(self):
		self.connection.root.exposed_unbeep()
	
	def close(self):
		self.connection.root.exposed_close()
	
class LocalAntilost(Antilost, threading.Thread):
	''' Locally connects to the antilost thing via BT '''

	def __init__(self, bt_device_adr):
		# call constructors
		Antilost.__init__(self, bt_device_adr)
		threading.Thread.__init__(self)
		# init variables
		self._device = None
		self._beep_req = False
		self._unbeep_req = False
		self._deactivate_noti_req = False
		self._activate_noti_req = False
		# notification
		self._notification = True
		
		# start the thread
		self.setDaemon(True)
		self.start()

	def connect(self):
		if (self._device == None):
			#print("Try connection to Antilost.")
			self._device = btle.Peripheral(self.bt_device_adr)
			#print("Connection to Antilost succeeded.")
			postopenhab.post_value_to_openhab("HavirInRange", "ON")
			if (self._notification):
				self._notification_active()
		
	def disconnect(self):
		if (self._device != None):
			self._device.disconnect()
			postopenhab.post_value_to_openhab("HavirInRange", "OFF")
			self._device = None

	def beep(self):
		self._beep_req = True

	def unbeep(self):
		self._unbeep_req = True

	def activate_notification(self):
		self._activate_noti_req = True
		
	def _notification_active(self):
		self._device.withDelegate(ButtonPressedDelegate())
		self._device.writeCharacteristic(noti_set_handle, binascii.a2b_hex('0100'))
		self._notification = True
		self._activate_noti_req = False
		
	def _notification_deactive(self):
		self._device.writeCharacteristic(noti_set_handle, binascii.a2b_hex('0000'))
		self._notification = False
		self._deactivate_noti_req = False
	
	def deactivate_notification(self):
		self._deactivate_noti_req = True

	def run(self):
		while True:
			try:
				self.connect()
				# receive notifications
				if (self._notification):
					self._device.waitForNotifications(0.3)
			
				# process requests
				if (self._beep_req):
					self._device.writeCharacteristic(beep_handle, binascii.a2b_hex('4041404361'))
					self._beep_req = False
				if (self._unbeep_req):
					self._device.writeCharacteristic(beep_handle, binascii.a2b_hex('6f6e6f6f4e'))
					self._unbeep_req = False
				if (self._activate_noti_req):
					_notification_active()
				if (self._deactivate_noti_req):
					_notification_deactive()
			except btle.BTLEException:
				# TODO my be unappropriate to catch all BTLEException. Probabyl only particular ones make sense. 
				self.disconnect()
				#print("Error: Communication to Havir lost.")
				time.sleep(5*60)
				
class ButtonPressedDelegate(btle.DefaultDelegate):
	''' React to pressing and releasing of the Havir button. '''
	
	def __init__(self):
		btle.DefaultDelegate.__init__(self)

	def handleNotification(self, cHandle, data):
		str = binascii.b2a_hex(data)
		if (cHandle == noti_recv_handle):
			if (str == "4140"):
				#print("pressed")
				postopenhab.post_value_to_openhab("HavirPressed", "ON")
			elif (str == "0000"):
				postopenhab.post_value_to_openhab("HavirPressed", "OFF")
				#print("released")
			else:
				print "Error: received wrong value"
		else:
			print "Error received from wrong handle"
	

class HavirBluetoothService(rpyc.Service):
	havir = None

	def on_connect(self):
		pass

	def on_disconnect(self):
		pass

	def exposed_beep(self):
		HavirBluetoothService.havir.beep()
		
	def exposed_unbeep(self):
		HavirBluetoothService.havir.unbeep()
	
	def exposed_close(self):
		sys.exit()
	
def main():
	parser = argparse.ArgumentParser(description="Control Havir BT item.")
	parser.add_argument("-a", dest = "address", metavar = "address", nargs = "?",
		help="MAC Address of the BT device.")
	parser.add_argument("-c", dest = "command", metavar = "command", nargs = "?",
		help="Options: beep, unbeep, server and close.")
	parser.add_argument("-t", dest = "time", metavar = "time", nargs = "?",
		help="Optional time if beep function is used.")
		
	args = parser.parse_args()
			
	# client commands
	if (args.command == 'beep') or (args.command == 'unbeep') or (args.command == 'close'):
		antilost = RemoteAntilost(args.address)
		if (not antilost.connect()):
			#print("Using localcall")
			antilost = LocalAntilost(args.address)
		if (args.command == 'beep'):
			antilost.beep()
			if not (args.time == None):
				time.sleep(float(args.time))
				antilost.unbeep()
		elif (args.command == 'unbeep'):
			antilost.unbeep()
		elif (args.command == 'close'):
			antilost.close()
			
	# server commands
	elif (args.command == 'server'):
		local_antilost = LocalAntilost(args.address)
		#print("starting antilost thread.")

		# store variable
		HavirBluetoothService.havir = local_antilost
			
		# start server
		from rpyc.utils.server import ThreadedServer
		t = ThreadedServer(HavirBluetoothService, port = bt_havir_port)
		#print("Starting server to listen")
		t.start()
			
		
if __name__ == "__main__":
	main()
