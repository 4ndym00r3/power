/*
 * 10/09/2019 - Andy Moore
 * Updated with interrupt 'de-bounce' due to interrupt sometimes
 * providing two interrupts per flash for the power led on the
 * meter
 *
 * This file was adapted and simplified from the example isr.c
 * distributed with wiringPi by Gordon Henderson
 *
 * It waits for an interrupt on GPIO 1 and prints 'Interrupt' to stdout
 * It is used with a python script to monitor pulses from a power meter
 * and report the usage to EmonCMS
 *
 * See here: http://github.com/kieranc/power/
 *
 * Copyright (c) 2013 Gordon Henderson.
 ***********************************************************************
 * This file is part of wiringPi:
 *	https://projects.drogon.net/raspberry-pi/wiringpi/
 *
 *    wiringPi is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    wiringPi is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
 ***********************************************************************
 */


#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <limits.h>
#include <wiringPi.h>
#include <time.h>
void myInterrupt() {
    printf ("Interrupt\n");
    fflush (stdout);

    // Debounce the interrupt by waiting for 250ms
    struct timespec ts;
    ts.tv_sec = 0;
    ts.tv_nsec = (250 % 1000) * 1000000;
    nanosleep(&ts, NULL);
}

/*
 *********************************************************************************
 * main
 *********************************************************************************
 */

int main (void)
{
  wiringPiSetup () ;

  wiringPiISR (4, INT_EDGE_FALLING, &myInterrupt) ;

  for (;;) {
        sleep(UINT_MAX);
    }
    return 0;
}
