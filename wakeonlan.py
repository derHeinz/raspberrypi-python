#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Library to use wake on lan.
Call me like this wakeonlan.py <Openhabitem> <Mac-for-wakeonla>.
"""

import sys
import subprocess
import postopenhab

if len(sys.argv) < 2 or None == sys.argv[1]:
    print("OFF")
else:
    item = sys.argv[1]
    mac = sys.argv[2]
    macWithColon = mac.replace("-", ":")
    
    val = postopenhab.get_switch_value_from_openhab(item)
    result = None
    if (val):
        # wakeonlan -p 9 00:11:22:33:44:55
        call_result = subprocess.call(["wakeonlan", "-p", "9", macWithColon], stdout=subprocess.PIPE)
        result = "ON"
    else:
        reult = "OFF"
    print(result)
