import time
import machine
from machine import Pin, I2C        
from time import sleep
import bme280                       

led = machine.Pin("LED", machine.Pin.OUT)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)

while True:
    led.toggle()
    print(bme.values)
   # write(bme.values)
    time.sleep(900)
    #15 minutes

