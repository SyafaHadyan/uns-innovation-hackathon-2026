import espnow
import framebuf
import network
import time
from machine import I2C, Pin

PLUG = b"\x40\x4c\xca\x3c\x5a\xa4"
ROUNDS = 10
GAP_MS = 1500


class SSD1306(framebuf.FrameBuffer):
    def __init__(self, i2c, addr=0x3C, width=128, height=64):
        self.i2c = i2c
        self.addr = addr
        self.w = width
        self.pages = height // 8
        self.buffer = bytearray(self.pages * width)
        super().__init__(self.buffer, width, height, framebuf.MONO_VLSB)
        init = (
            0xAE,
            0x20,
            0x00,
            0x40,
            0xA1,
            0xA8,
            height - 1,
            0xC8,
            0xD3,
            0x00,
            0xDA,
            0x12,
            0xD5,
            0x80,
            0xD9,
            0xF1,
            0xDB,
            0x30,
            0x81,
            0xFF,
            0xA4,
            0xA6,
            0x8D,
            0x14,
            0xAF,
        )
        for cmd in init:
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytes([0x80, cmd]))

    def show(self):
        for cmd in (0x21, 0, self.w - 1, 0x22, 0, self.pages - 1):
            self.write_cmd(cmd)
        self.i2c.writevto(self.addr, [b"\x40", self.buffer])


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306(i2c)


def show_lines(lines):
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 12)
    oled.show()


sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)
try:
    e.add_peer(PLUG)
except OSError:
    pass


def flush():
    while True:
        mac, msg = e.recv(0)
        if mac is None:
            break


show_lines(["WATTLINK HUB", "CMD   --", "RTT   --", "ACK   0/0", "RELAY --"])
time.sleep_ms(1500)

sent = 0
acked = 0
times = []

for i in range(ROUNDS):
    cmd = b"ON" if i % 2 == 0 else b"OFF"
    name = cmd.decode()
    sent += 1
    flush()
    t0 = time.ticks_us()
    e.send(PLUG, cmd, True)
    mac, msg = e.recv(500)
    dt = time.ticks_diff(time.ticks_us(), t0) / 1000
    if msg == cmd:
        acked += 1
        times.append(dt)
        rtt = "%.2f ms" % dt
        state = name
    else:
        rtt = "timeout"
        state = "?"
    show_lines(
        [
            "WATTLINK HUB",
            "CMD   " + name,
            "RTT   " + rtt,
            "ACK   " + str(acked) + "/" + str(sent),
            "RELAY " + state,
        ]
    )
    print(i + 1, name, rtt)
    time.sleep_ms(GAP_MS)

if times:
    avg = sum(times) / len(times)
    avg_text = "%.2f ms" % avg
else:
    avg_text = "--"

show_lines(
    [
        "WATTLINK HUB",
        "DONE",
        "ACK   " + str(acked) + "/" + str(sent),
        "AVG   " + avg_text,
    ]
)
print("done", acked, "of", sent, "avg", avg_text)
