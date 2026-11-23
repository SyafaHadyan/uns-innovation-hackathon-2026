from machine import UART, Pin
import time

uart = UART(1, baudrate=9600, tx=Pin(6), rx=Pin(7))

for i in range(5):
    uart.write(b"ping")
    time.sleep(0.2)
    print(uart.read())
