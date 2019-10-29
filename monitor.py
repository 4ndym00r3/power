#!/usr/bin/python

"""
	10/09/2019 - Andy Moore
	Updated Scheduler and EmonCMS URL due to bugs preventing correct operation
	of the application

	Modified by KieranC to submit pulse count to Open Energy Monitor EmonCMS API

	Power Monitor
	Logs power consumption to an SQLite database, based on the number
	of pulses of a light on an electricity meter.

	Copyright (c) 2012 Edward O'Regan

	Permission is hereby granted, free of charge, to any person obtaining a copy of
	this software and associated documentation files (the "Software"), to deal in
	the Software without restriction, including without limitation the rights to
	use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
	of the Software, and to permit persons to whom the Software is furnished to do
	so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
"""

import time, os, subprocess, httplib, datetime
from apscheduler.schedulers.background import BackgroundScheduler

pulsecount=0
power=0

# Every minute this function converts the number of pulses over the last minute into a power value and sends it to EmonCMS
# @sched.interval_schedule(minutes=1)
def SendPulses():
	global pulsecount
	global power
#	print ("Pulses: %i") % pulsecount # Uncomment for debugging.

# 	Calculate power value in watts from the number of pulses, power = pulsecount/min * ((3600/meter pulses per kWh)*16.6667W/min)
	power = pulsecount * 60

#	print ("Power: %iW") % power # Uncomment for debugging.
	pulsecount = 0
	timenow = time.strftime('%s')

#	You'll need to put in your API key here from EmonCMS
        url = ("/input/post?node=<insert node name here>&time=%s&json={power1:%i}&apikey=<insert api key here>") % (timenow, power)
        connection = httplib.HTTPSConnection("emoncms.org")
        connection.request("GET", url)

# Start the scheduler
sched = BackgroundScheduler()
sched.add_job(SendPulses, 'interval', seconds=60)
sched.start()


# This function monitors the output from gpio-irq C app
# Code from vartec @ http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
def runProcess(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
      retcode = p.poll() #returns None while subprocess is running
      line = p.stdout.readline()
      yield line
      if(retcode is not None):
        break

for line in runProcess(["/root/power/gpio-new"]):
    pulsecount += 1
