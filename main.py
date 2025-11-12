import time
import machine
from machine import Pin, I2C        # importing relevant modules & classes
from time import sleep
import bme280                       # importing BME280 library

# Set up LED
led = machine.Pin("LED", machine.Pin.OUT)

# Initialize I2C for BME280
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)  # Initialize BME280 once

while True:
    # Toggle the LED
    led.toggle()
    
    # Read from BME280 sensor and print values
    print(bme.values)
    
    # Sleep for a specified time
    time.sleep(1.5)  # You can adjust this sleep time as needed
    

