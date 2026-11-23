import network
import espnow
import time

PLUG = b"\x40\x4c\xca\x3c\x5a\xa4"

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)
e.add_peer(PLUG)

for i in range(10):
    cmd = b"on" if i % 2 == 0 else b"off"
    t0 = time.ticks_us()
    e.send(PLUG, cmd)
    mac, msg = e.recv(1000)
    t1 = time.ticks_us()
    if msg == cmd:
        print(cmd, "round trip ms:", time.ticks_diff(t1, t0) / 1000)
    else:
        print(cmd, "no ack")
    time.sleep(1)
