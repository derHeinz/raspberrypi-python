#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import traceback

errorlog_file = "errors.log"

def write_to_errorlog(text):
    now = datetime.datetime.now().isoformat()
    f = open(errorlog_file, 'a')
    f.write(str(now) + " ERROR " + text)
    f.write('\n')
    f.close()

def error_happened(exc):
    tb = traceback.format_exc()
    write_to_errorlog(str(tb))
