#!/usr/bin/python
# -*- coding: utf-8 -*-

# you need current bluez: http://raspberrypi.stackexchange.com/questions/39254/updating-bluez-5-23-5-36

from bluepy.btle import Scanner, DefaultDelegate

class BTThermometerDelegate(DefaultDelegate):
	def __init__(self, bt_addr):
		DefaultDelegate.__init__(self)
		self.bt_addr = bt_addr

	def handleDiscovery(self, dev, isNewDev, isNewData):
		# ignore other devices
		if (dev.addr.upper() != self.bt_addr.upper()):
			return
		self.processData(dev)
		
	def processData(self, scanentry):
		print(scanentry.getScanData())
		print(scanentry.getValueText(9))
		print(scanentry.getValueText(22))
		

#scanner = Scanner().withDelegate(BTThermometerDelegate("C4:B3:61:94:78:38"))
#while True:
#devices = scanner.scan()


from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    for (adtype, desc, value) in dev.getScanData():
        print "  %s = %s" % (desc, value)

