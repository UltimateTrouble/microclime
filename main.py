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
    current_time = time.localtime()
    hour = current_time[3]
    minute = current_time[4]
    if (minute == 0 or minute == 30):
        data = bme.values
        timestamp_string = f"{current_time[0]:04}-{current_time[1]:02}-{current_time[2]:02} {hour:02}:{minute:02}:{current_time[5]:02}"
        data_string = f"{timestamp_string}, Temperature: {data[0]}, Pressure: {data[1]}, Humidity: {data[2]}\n"
        with open(datafile, "a") as file:
            file.write(data_string)
        time.sleep(60)
    time.sleep(1)
