#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import pexpect
import subprocess
import os
import postopenhab

from subprocess import check_output, call

#######################
# PULSEAUDIO section
#######################

pulseaudio_pacmd = "/opt/openhab/configurations/scripts/pa-pacmd.sh"
sound_dir = "/opt/openhab/sounds/"

def paPlayMediaFromOpenhab(mediafile, sinkIndex):
	print "playing audio file: " + mediafile
	call([pulseaudio_pacmd, "play-file", sound_dir + mediafile, sinkIndex])

def paRunning():
	try:
		subprocess.check_call(["pulseaudio", "--check"])
		return True
	except subprocess.CalledProcessError as cpe:
		return False

def paFindSinkIndexForMac(mac):
	index = "index:"
	sinksString = check_output([pulseaudio_pacmd, "list-sinks"])
	macLocation = sinksString.find(mac)
	if (macLocation == -1):
		return "0"

	# where the "index: " is located
	sinkStringIndex = 0

	occurence = 0
	while occurence < len(sinksString):
		occurence = sinksString.find(index, occurence)
		if occurence == -1:
			break
	
		if (((macLocation - occurence) > 0) and ((macLocation - occurence) > sinkStringIndex)):
			sinkStringIndex = occurence
	
		occurence += len(index)

	substr = sinksString[sinkStringIndex:]
	indexBegin = substr .find(":")
	indexEnd = substr.find("\n")
	substr = substr[indexBegin+1:indexEnd]
	return substr

def paMakeSoundOutputToSink(sinkNumber):
	call([pulseaudio_pacmd, "set-default-sink", sinkNumber]) 

#######################
# BLUETOOTH section:
#######################

def speakerConnected(mac):
	child = pexpect.spawn('bluetoothctl')
	child.expect('\# ')             #bluetoothctl zeigt # und ein Leerzeichen an i$
	child.sendline('info ' + mac)
	connected = False
	try:
		for line in child: 
			if ("Connected: " in line):
				indexBegin = line.find(":")
				indexEnd = line.find("\n")
				substr = line[indexBegin+1:indexEnd]
				if ("yes" in substr):
					connected = True
				break
		child.sendline('quit')	
	except pexpect.exceptions.TIMEOUT as cpe:
		return False
	return connected 

def connectSpeaker(mac):
	try:
		child = pexpect.spawn('bluetoothctl')
		child.expect('\# ')             #bluetoothctl zeigt # und ein Leerzeichen an i$
		child.sendline('agent NoInputNoOutput') # damit kein passkey notwendig ist für das Pairing
		child.expect('\# ')
		child.sendline('power on')
		child.expect('\# ')
		child.sendline('agent on')
		child.expect('\# ')
		child.sendline('scan on')
		time.sleep(3)                    #scan abwarten
		child.expect('\# ')
		child.sendline('scan off')
		child.expect('\# ')
		child.sendline('pair ' + mac)
		child.expect('\# ')
		child.sendline('trust ' + mac)
		child.expect('\# ')
		child.sendline('connect ' + mac)
		#child.expect('\# ')
		child.expect('Connection successful')
		child.sendline('quit')
		return True
	except pexpect.exceptions.TIMEOUT as cpe:
		return False

def disconnectSpeaker(mac):
	child = pexpect.spawn('bluetoothctl')
	child.expect('\# ') 
	child.sendline('disconnect ' + mac)
	#child.expect('\# ')
	child.expect('Successful disconnected')
	child.sendline('quit')

def procedureEnableSpeaker(mac):
	print "connecting to mac: " + mac
	connectSpeaker(mac)
	sinkNumber = findSinkIndexForMac(mac)
	print "setting default pulseaudio sink to " + sinkNumber
	makeSoundOutputToSink(sinkNumber)
	
# Library function
def playSound(mac, soundfile):
	# Common procedure:
	# 0. Get the input MAC and input audio file.
	macWithColon = mac.replace("-", ":")

	# 1. check pulseaudio running
	# 2. if pulseaudio not running start it
	#if (not paRunning()):
	#	call(["pulseaudio", "--system", "-D"])

	# 3. check if the BT speaker is connected
	# 4. if BT speaker not connected connect it.
	
	if (not speakerConnected(macWithColon)):
		if (not connectSpeaker(macWithColon)):
			postopenhab.post_systemnotification("BT-Speaker", "bt-speaker not responding")
			return

	#time.sleep(2)

	# 5. check if BT speaker is default sink for pulseaudio
	# 6. if BT speaker is not default sink set it so
	sinkNumber = paFindSinkIndexForMac(macWithColon)
	#makeSoundOutputToSink(str(sinkNumber))

	#time.sleep(2)

	# 7. play media file
	paPlayMediaFromOpenhab(soundfile, str(sinkNumber))