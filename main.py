import time
import socket
import network
import machine
from machine import Pin, I2C        
import bme280                       

ssid = 'TP-Link_3B00'
password = '67783076'

led = machine.Pin(15, machine.Pin.OUT)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)
datafile = "data.txt"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    
    try:
        connection.bind(address)
        connection.listen(1)
        return connection
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print("Address already in use. Retrying...")
            time.sleep(2)  # Wait a moment before retrying
            return open_socket(ip)  # Try binding again
        else:
            print(f"Socket error: {e}")
            connection.close()
            raise

def webpage(reading):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>Pico 2W Weather Station</title>
        <meta http-equiv="refresh" content="10">
        </head>
        <body>
        <p>{reading}</p>
        </body>
        </html>
    """
    return str(html)

def serve(connection):
    while True:
        try:
            temp, pressure, humidity = bme.values
            reading = f'Temperature: {temp}, Humidity: {humidity}, Pressure: {pressure}'
            client = connection.accept()[0]
            request = client.recv(1024)
            html = webpage(reading)
            client.send(html)
            client.close()
            led.toggle()

        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(1)          
# Main execution
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    print("Program stopped by user.")
except OSError as e:
    print(f"Failed to start server: {e}")
finally:
    if 'connection' in locals() and connection:
        connection.close()
        print("Socket closed.")
        
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
