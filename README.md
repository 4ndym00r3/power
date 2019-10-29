power
=====

Electricity power meter monitoring directly on the Pi using Open Energy Monitor and an LDR. This code polls your power meter and logs the power usage per minute. This is determined by monitoring the number of impulses or flashes per minute via the impulse indicator on the meter. The power value in Watts is sent to EmonCMS, the open source energy monitoring CMS provided by the Open Energy Monitor project.

I've forked this from KieranC's power meter (https://github.com/kieranc/power) which was forked from yfory's power meter: (https://github.com/yfory/power).

Details
=======

yfory used a capacitor/resistor for the detection LDR, whereas KieranC used a transistor based circuit instead to provide a digital on/off signal which I also used. KieranC also interfaces directly to EmonCMS which provides an easy solution to graph power monitoring and provide cumulative and instananeous power readouts via the EmonCMS UI. EmonCMS is an open source energy monitoring solution provided by the OpenEnergyMonitor project (see https://openenergymonitor.org/). You can run EmonCMS locally on a Raspberry Pi or use the cloud solution which is what I decided to do. You need to pay for a feed, though this is pretty cheap at around £1 per feed per year.

# Requirements
* Raspberry Pi
* Photoresistor (Light Dependent Resistor)
* 10k Ohm resistor
* 1k resistors
* NPN Transistor - I used a BC547
* Relevant Cables/Connectors
* Modern Electricity Meter

Modern electricity meters have a blinking/flashing LED, often with small text that reads '1000 Imp/kWh'. The two important things here are that you have a blinking LED on the meter that registers the power usage, and that you know the number of blinks (or Impulses) per kWh (e.g. 800). Without this capability you will not be able to monitor the electricity meter with this project.

This code is set up for 1000 Impulses/kWh, the multiplication factor of 60 sets this. 72 should work for 800 Impulses/kWh or 30 for 2000 Impulses/kWh. To calculate the multiplication factor to convert pulses to Watts use the following equation:

```bash
multiplication factor (mf) = ((3600/meter pulses per kWh)*16.6667W/min)
```
therefore:

```bash
power = pulsecount/min * mf
```

This project uses the LDR as one half of a voltage divider to trigger a transistor which is connected to a GPIO pin on the Pi.

The circuit is documented here: http://pyevolve.sourceforge.net/wordpress/?p=2383

# Software Installation
On your Raspberry Pi, you will need to ensure that you have certain Python related files installed. To make sure, type the following commands...

```bash
sudo apt-get install python-dev python-pip
sudo pip install apscheduler RPi.GPIO
```

The above installs the advanced python scheduler and RPi GPIO tools used by the code.
Now you will want to download the files from this github repository. To do so, type the following commands...
(KieranC's code refered to /root/power for the home directory for the code so I've kept with that premise, though changed the instructions slightly to ensure the code is downloaded into this directory when cloned)

```bash
sudo apt-get install git wiringpi gcc
sudo mkdir /root && cd /root
sudo git clone https://github.com/4ndym00r3/power.git && cd power
```

(I think that should install all the major files, though let me know if you need to install anything else as I had to install several packages that were not originally spec'd by KieranC and I can't remember all the packages I needed!)

The file named power-monitor is used to automatically start the data logging process on boot and stop on shutdown. For testing purposes, you do not need this script. However, you should make use of it if you are setting up a more permanent solution.

```bash
sudo cp power-monitor /etc/init.d/
sudo chmod a+x /etc/init.d/power-monitor
sudo update-rc.d power-monitor defaults
```

**Note:** Be sure to check the power-monitor file to make sure that the path to the Python application, monitor.py, matches with the path on your system. For example, /root/power/power.py

Due to Python's inability to respond to an interrupt, I've used a very simple C app to listen for an interrupt triggered when the LDR detects a pulse. Monitor.py counts these pulses and each minute, creates a power reading in watts which it sends to EmonCMS' API.
This file was adapted and simplified from the example isr.c distributed with wiringPi by Gordon Henderson
This app will need compiling like so:

```bash
gcc gpio-new.c -o gpio-new -lwiringPi
```

Put it somewhere accessible - I used /root/power, this will need modifying at the bottom of monitor.py if you put it somewhere else.

Once all this is done you can start the data logging process...

```bash
sudo /etc/init.d/power-monitor start
```

You can read how to set up EmonCMS on the Pi here: https://guide.openenergymonitor.org/technical/api/

Once you have set up EmonCMS you will need to get your API key and put it in monitor.py, line 56.

You then create a feed to accept the input. This is where the data is logged. You can then create a graph to view the feed.


# License

Copyright (c) 2012 Edward O'Regan with updates (c) 2019 Andy Moore

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

