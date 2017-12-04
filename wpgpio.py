"""
Library for working with GPIOs.
"""

import argparse
import sys
import wiringpi
import time

class GPIOAccess:
	"""Access to gpios via wiringpi2"""
	
	def __init__(self):
		self.setupDone = False
	
	def _setup(self):
		if not (self.setupDone):
			wiringpi.wiringPiSetupGpio()
			self.setupDone = True
	
	def read(self, gpio):
		self._setup()
		wiringpi.pinMode(gpio, 0)
		state = wiringpi.digitalRead(gpio)
		return state
		
	def write(self, gpio, state):
		self._setup()
		wiringpi.pinMode(gpio, 1)
		wiringpi.digitalWrite(gpio, state)
		
	def switch_off_on(self, gpio, timeout):
		self._setup()
		wiringpi.pinMode(gpio, 1)
		wiringpi.digitalWrite(gpio, 0)
		time.sleep(timeout)
		wiringpi.digitalWrite(gpio, 1)
		
	def switch_on_off(self, gpio, timeout):
		self._setup()
		wiringpi.pinMode(gpio, 1)
		wiringpi.digitalWrite(gpio, 1)
		time.sleep(timeout)
		wiringpi.digitalWrite(gpio, 0)
		
def main():
	parser = argparse.ArgumentParser(description="DO sth. with GPIOs.")
	parser.add_argument("-g", dest = "gpio", type=int, metavar = "gpio", nargs = "?", help="GPIO to do.")
	parser.add_argument("-c", dest = "command", metavar = "command", nargs = "?", help="Command to issue: read-con, read-sw, set, pulldown, off-on, on-off")
	parser.add_argument("-t", dest = "time", metavar = "time", nargs = "?", help="Optional time.")
	parser.add_argument("-v", dest = "value", metavar = "value", nargs = "?", help="Optional value to set.")

	args = parser.parse_args()
	
	gpio_access = GPIOAccess()
	gpio_access._setup()
	
	if (args.command == 'set'):
		what = "Sets GPIO to value given."
		if args.value in ["off"]:
			gpio_access.write(args.gpio, 0)
		elif args.value in ["on"]:
			gpio_access.write(args.gpio, 1)
	elif (args.command == 'off-on'):
		what = "Pulldown and on again for time GPIO."
		gpio_access.switch_off_on(args.gpio, float(args.time))
	elif (args.command == 'on-off'):
		what = "Pulldown and on again for time GPIO."
		gpio_access.switch_on_off(args.gpio, float(args.time))
	elif (args.command == 'read-con'):
		what = "Read GPIO and return text for Contact."
		state = gpio_access.read(args.gpio)
		if 0 == state:
			print 'CLOSED'
		else:
			print 'OPEN'
	elif (args.command == 'read-sw'):
		what = "Read GPIO and return text for Switch."
		state = gpio_access.read(args.gpio)
		if 0 == state:
			print 'OFF'
		else:
			print 'ON'
	
		
if __name__ == "__main__":
	main()
