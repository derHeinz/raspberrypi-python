import unittest
import scan_results
import binascii
import struct

class BatteryServiceResultTest(unittest.TestCase):
    
	def test_translate(self):
		t = binascii.a2b_hex("0f1825")
		s = binascii.b2a_hex(t)
		self.assertEquals("0f1825", s)
		
	def test_is_type(self):
		# valid one
		t = binascii.a2b_hex("0f1825")
		self.assertEquals(True, scan_results.BatteryServiceResult.is_type(22, t))
		# wrong values
		t = binascii.a2b_hex("123425")
		self.assertEquals(False, scan_results.BatteryServiceResult.is_type(22, t))
		# switched values
		t = binascii.a2b_hex("180f25")
		self.assertEquals(False, scan_results.BatteryServiceResult.is_type(22, t))
		# no values
		t = binascii.a2b_hex("05")
		self.assertEquals(False, scan_results.BatteryServiceResult.is_type(22, t))
		
	def test_parse_value(self):
		# valid one
		t = binascii.a2b_hex("0f1825")
		res = scan_results.BatteryServiceResult(22, t)
		self.assertEquals("37", res.get_battery_level()) #0x25 = 37
		
		
class HealthThermometerResultTest(unittest.TestCase):
		
	def test_is_type(self):
		# valid one
		t = binascii.a2b_hex("0918a10800fe")
		self.assertEquals(True, scan_results.HealthThermometerResult.is_type(22, t))
		# wrong values
		t = binascii.a2b_hex("0118a10800fe")
		self.assertEquals(False, scan_results.HealthThermometerResult.is_type(22, t))
		# switched values
		t = binascii.a2b_hex("1809a10800fe")
		self.assertEquals(False, scan_results.HealthThermometerResult.is_type(22, t))
		# too short
		t = binascii.a2b_hex("1809a10800")
		self.assertEquals(False, scan_results.HealthThermometerResult.is_type(22, t))
		
	def test_parse_value(self):
		# valid one
		t = binascii.a2b_hex("0918a10800fe")
		res = scan_results.HealthThermometerResult(22, t)
		self.assertEquals(22.09, res.get_temperature())

if __name__ == '__main__':
	unittest.main()