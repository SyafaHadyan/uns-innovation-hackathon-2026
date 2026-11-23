import network
import espnow
from machine import Pin

HUB = b"\x48\xe7\x29\xb6\xe0\x84"

relay = Pin(3, Pin.OUT, value=0)

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)
e.add_peer(HUB)

print("plug ready")

while True:
    mac, msg = e.recv(1000)
    if msg is None:
        continue
    if msg == b"on":
        relay.value(1)
    elif msg == b"off":
        relay.value(0)
    else:
        continue
    e.send(HUB, msg)
    print(msg)
