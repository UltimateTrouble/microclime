import time
import machine
from machine import Pin, I2C        
import bme280                       

led = machine.Pin("LED", machine.Pin.OUT)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)
datafile = "data.txt"  

while True:
    led.toggle()
    data = bme.values
    timestamp = time.localtime()
    timestamp_string = f"{timestamp[0]:04}-{timestamp[1]:02}-{timestamp[2]:02} {timestamp[3]:02}:{timestamp[4]:02}:{timestamp[5]:02}"
    data_string = f"{timestamp_string}, Temperature: {data[0]}, Pressure: {data[1]}, Humidity: {data[2]}\n"
    with open(datafile, "a") as file:
        file.write(data_string)
    time.sleep(1800)  # Sleep for 15 minutes (1800 seconds)
