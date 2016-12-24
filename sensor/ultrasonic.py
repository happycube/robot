##
# Ultrasonic library for MicroPython's pyboard.
# Compatible with HC-SR04 and SRF04.
#
# Copyright 2014 - Sergio Conde Gómez <skgsergio@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# cpage - adapted 12/24/2016 to work on MicroPython on ESP8266, and added
# code to handle timing errors (RTOS preemption related?)
##

import machine 
import time 

from machine import Pin

class Ultrasonic:
    def __init__(self, tPin, ePin):
        self.triggerPin = tPin
        self.echoPin = ePin

        # Init trigger pin (out)
        self.trigger = Pin(self.triggerPin)
        self.trigger.init(Pin.OUT, None)
        self.trigger.low()

        # Init echo pin (in)
        self.echo = Pin(self.echoPin)
        self.echo.init(Pin.IN, None)

    def distance_in_inches(self):
        return (self.distance_in_cm() * 0.3937)

    def distance_in_cm(self):
        start = 0

        # Send a 10us pulse.
        self.trigger.high()
        time.sleep_us(10)
        self.trigger.low()
   
	first_start = time.ticks_us()

        iters = 0
        # Wait 'till whe pulse starts.
        while self.echo.value() == 0:
            start = time.ticks_us()
            iters += 1

            if ((iters % 10000) == 0) and (time.ticks_diff(start, first_start) > 50000):
                return -1

        end = time.ticks_us()
        iters = 0
        # Wait 'till the pulse is gone.
        while (self.echo.value() == 1):
            end = time.ticks_us()
            iters += 1

            if ((iters % 10000) == 0) and (time.ticks_diff(end, start) > 100000):
                return -2

        # Calc the duration of the recieved pulse, divide the result by
        # 2 (round-trip) and divide it by 29 (the speed of sound is
        # 340 m/s and that is 29 us/cm).
        dist_in_cm = (time.ticks_diff(end, start) / 2) / 29

        if (dist_in_cm > 1000):
            return -3

        return dist_in_cm
