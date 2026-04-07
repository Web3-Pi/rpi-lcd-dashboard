# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import sys
import time
import spidev
import logging
import numpy as np
from gpiozero import DigitalOutputDevice, PWMOutputDevice, DigitalInputDevice
from gpiozero.pins.lgpio import LGPIOFactory


SPI_BUS = int(os.environ.get('SPI_BUS', 10))
SPI_DEVICE = int(os.environ.get('SPI_DEVICE', 0))
SPI_SPEED = int(os.environ.get('SPI_SPEED', 10000000))
GPIO_CHIP = int(os.environ.get('GPIO_CHIP', 0))
DIGITAL_BACKLIGHT = os.environ.get('DIGITAL_BACKLIGHT', 'true').lower() == 'true'

print("Python initialized with dynamically injected HA Add-on parameters.")

# Globally override gpiozero's Pi 5 chip detection bug
Device.pin_factory = LGPIOFactory(chip=GPIO_CHIP)

class RaspberryPi:
def __init__(self, spi_freq=SPI_SPEED, rst=27, dc=25, bl=18, bl_freq=1000, i2c=None, i2c_freq=100000):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Apply the dynamic SPI parameters
        self.spi = spidev.SpiDev(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = spi_freq
        self.spi.mode = 0  # Force Mode 0 for the ST7789 chip
        
        # Apply the Backlight patch dynamically
        if DIGITAL_BACKLIGHT:
            self._pwm = DigitalOutputDevice(bl)
            self._pwm.value = 1
        else:
            self._pwm = PWMOutputDevice(bl, frequency=bl_freq)
            self._pwm.value = 1.0

        self.np = np
        self.INPUT = False
        self.OUTPUT = True

        self.SPEED = spi_freq
        self.BL_freq = bl_freq

        self.RST_PIN = self.gpio_mode(rst, self.OUTPUT)
        self.DC_PIN = self.gpio_mode(dc, self.OUTPUT)
        self.BL_PIN = self.gpio_pwm(bl)
        self.bl_DutyCycle(0)

        # Initialize SPI
        self.SPI = spi
        if self.SPI != None:
            self.SPI.max_speed_hz = spi_freq
            self.SPI.mode = 0b00

    def gpio_mode(self, Pin, Mode, pull_up=None, active_state=True):
        if Mode:
            return DigitalOutputDevice(Pin, active_high=True, initial_value=False, pin_factory=factory)
        else:
            return DigitalInputDevice(Pin, pull_up=pull_up, active_state=active_state, pin_factory=factory)

    def digital_write(self, Pin, value):
        if value:
            Pin.on()
        else:
            Pin.off()

    def digital_read(self, Pin):
        return Pin.value

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def gpio_pwm(self, Pin):
        return DigitalOutputDevice(Pin)

    def spi_writebyte(self, data):
        if self.SPI != None:
            self.SPI.writebytes(data)

    def bl_DutyCycle(self, duty):
        self.BL_PIN.value = duty / 100

    def bl_Frequency(self, freq):  # Hz
        self.BL_PIN.frequency = freq

    def module_init(self):
        if self.SPI != None:
            self.SPI.max_speed_hz = self.SPEED
            self.SPI.mode = 0b00
        return 0

    def module_exit(self):
        logging.debug("spi end")
        if self.SPI != None:
            self.SPI.close()

        logging.debug("gpio cleanup...")
        self.digital_write(self.RST_PIN, 1)
        self.digital_write(self.DC_PIN, 0)
        self.BL_PIN.close()
        time.sleep(0.001)


'''
if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
'''

### END OF FILE ###
