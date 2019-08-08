#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import traceback

errorlog_file = "errors.log"

def write_to_errorlog(text):
    f = open(errorlog_file, 'a')
    f.write(text)
    f.write('\n')
    f.close()

def error_happened(exc):
    tb = traceback.format_exc()
    now = datetime.datetime.now().isoformat()
    write_to_errorlog(str(now) + " " + str(tb))
