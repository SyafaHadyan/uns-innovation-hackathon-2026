import espnow
import network
from machine import Pin

HUB = b"\x48\xe7\x29\xb6\xe0\x84"

# Keep the relay off before anything else
relay = Pin(3, Pin.OUT, value=0)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)
try:
    e.add_peer(HUB)
except OSError:
    pass

print("plug ready, waiting for commands")

while True:
    mac, msg = e.recv(1000)
    if msg is None:
        continue
    if msg == b"ON":
        relay.value(1)
    elif msg == b"OFF":
        relay.value(0)
    else:
        continue
    # Echo the command so the Hub can measure the round trip
    e.send(mac, msg, True)
    print(msg, relay.value())
