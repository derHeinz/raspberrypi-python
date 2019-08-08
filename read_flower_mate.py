#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from bluepy import btle
import binascii

class MiFlowerMate():

    MI_TEMPERATURE = "temperature"
    MI_LIGHT = "light"
    MI_MOISTURE = "moisture"
    MI_CONDUCTIVITY = "conductivity"
    MI_BATTERY = "battery"
    
    def __init__(self, bt_device_adr):
        self._device = None
        if ("-" in bt_device_adr):
            self.bt_device_adr = bt_device_adr.replace("-", ":")
        else:
            self.bt_device_adr = bt_device_adr
    
    def _connect(self):
        if (self._device == None):
            self._device = btle.Peripheral(self.bt_device_adr)
            
    def _disconnnect(self):
        if (self._device != None):
            try:
                self._device.disconnect()
            except (btle.BTLEException, IOError):
                pass # may happen we don't care
            self._device = None
    
    def _parse_data(self, data):
        res = {}
        res[self.MI_TEMPERATURE] = float(data[1] * 256 + data[0]) / 10
        res[self.MI_MOISTURE] = data[7]
        res[self.MI_LIGHT] = data[4] * 256 + data[3]
        res[self.MI_CONDUCTIVITY] = data[9] * 256 + data[8]
        return res
    
    def _chars_to_intarray(self, data):
        result = []
        result_str = ""
        count = -1
        for i in data:
            count += 1
            if count>0 and count%2==0:
                result.append(int(result_str, 16))
                result_str = ""
            result_str += i        
        return result
    
    def get_information(self):
        self._connect()
        charact_result = self._device.readCharacteristic(0x035) #characteristic containing information
        charact_result_ascii = binascii.b2a_hex(charact_result)
        charact_result_ints = self._chars_to_intarray(charact_result_ascii)
        results = self._parse_data(charact_result_ints)
        self._disconnnect()
        return results
