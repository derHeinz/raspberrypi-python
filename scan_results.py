import struct
import binascii

# https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile
class SingleResult(object):
	"""Result portion if not defined yet."""
	
	def __init__(self, sdid, val):
		self.sdid = sdid
		self.val = val
		self._parse(val)

	def _parse(self, val):
		pass

	@staticmethod
	def is_type(sdid, val):
		return True

	def pretty_print(self):
		sb = []
		for key in self.__dict__:
			sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
		return (str(type(self)) + " " + ', '.join(sb))

class LocalNameResult(SingleResult):
	"""The name of the device."""
	
	def __init__(self, sdid, val):
		super(LocalNameResult, self).__init__(sdid, val)
		
	@staticmethod
	def is_type(sdid, val):
		if sdid == 9:
			return True
		return False
		
	def get_name(self):
		return self.val

# see: https://www.bluetooth.com/specifications/gatt/services
class ServiceResult(SingleResult):
	"""16bit Service result."""
	
	def __init__(self, sdid, val):
		super(ServiceResult, self).__init__(sdid, val)

	def _parse(self, val):
		number_of_bytes = len(val) / 2
		bs = 'B' * number_of_bytes
		self.bytes = struct.unpack_from('<' + bs, val)

	@staticmethod
	def is_type(sdid, val):
		if sdid == 0x16:
			return True
		return False

# https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.service.battery_service.xml
class BatteryServiceResult(ServiceResult):
	"""Battery level service."""
	
	def __init__(self, sdid, val):
		super(BatteryServiceResult, self).__init__(sdid, val)
		
	def _parse(self, val):
		as_string = binascii.b2a_hex(val)[-2:]
		as_hex_int = int(as_string, 16)
		self.battery_level = str(as_hex_int)

	@staticmethod
	def is_type(sdid, val):
		if not super(BatteryServiceResult, BatteryServiceResult).is_type(sdid, val):
			return False
			
		if len(val) < 3: # needs to be 3 values, the first two are the type the last ist the actual value
			return False
		return ((0x0F, 0x18)==struct.unpack_from('<BB', val))
		
	def get_battery_level(self):
		return self.battery_level
	

# https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.service.health_thermometer.xml
class HealthThermometerResult(ServiceResult):
	"""Thermometer service."""
	
	def __init__(self, sdid, val):
		super(HealthThermometerResult, self).__init__(sdid, val)
		
	def _parse(self, val):
		as_string = binascii.b2a_hex(val)
		
		temperature = as_string[4:-2]
		first = int(temperature[:-4], 16)
		second = int(temperature[2:-2], 16) * 256
		third = int(temperature[4:], 16) * 65536
		
		self.temperature = (first + second + third) / float(100)
		
	@staticmethod
	def is_type(sdid, val):
		if not super(HealthThermometerResult, HealthThermometerResult).is_type(sdid, val):
			return False
		if len(val) < 6:
			return False
		return ((0x09, 0x18)==struct.unpack_from('<BB', val))
		
	def get_temperature(self):
		return self.temperature
		
class ScanResult(object):
	"""Result object of device containig all it's data."""
	
	def __init__(self, parts):
		self.parts = parts
		
	def get_parts(self):
		return self.parts
		
	def get_services(self):
		return filter(lambda x: isinstance(x, SingleServiceResult), self.parts)
		
	def get_name(self):
		for part in self.parts:
			if isinstance(part, LocalNameResult):
				return part.get_name()
		
parse_order = [HealthThermometerResult, BatteryServiceResult, ServiceResult, LocalNameResult, SingleResult]

class ScanResultParser(object):
	"""Parses the scan result from device."""

	def process_device_raw_data(self, some_data):
		data = some_data
		# recalculate the service data
		results = []
		while len(data) >= 2:
			sdlen, sdid = struct.unpack_from('<BB', data)
			val = data[2 : sdlen + 1]
			results.append(self.create_result(sdid, val))
			data = data[sdlen + 1:]
			
		return ScanResult(results)

	def create_result(self, sdid, val):
		for res in parse_order:
			if res.is_type(sdid, val):
				return res(sdid, val)