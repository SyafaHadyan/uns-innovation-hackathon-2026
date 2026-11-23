from machine import Pin
import time

relay = Pin(3, Pin.OUT, value=0)

for _ in range(3):
    relay.value(1)
    print("relay on")
    time.sleep(2)
    relay.value(0)
    print("relay off")
    time.sleep(2)
