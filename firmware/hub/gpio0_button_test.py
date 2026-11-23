import sys
import time

import serial

PORT = "/dev/ttyUSB0"
RUN_SECONDS = 40

# Code that runs on the ESP32 (MicroPython v1.29.0 bench firmware).
# GPIO 0 is the BOOT button. Idle reads 1, pressed reads 0.
CODE = r"""
import time, framebuf
from machine import Pin, SoftI2C
W, H, ADDR = 128, 64, 0x3C
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
def cmd(c):
    i2c.writeto(ADDR, bytes([0x80, c]))
for c in (0xAE,0x20,0x00,0x40,0xA1,0xA8,H-1,0xC8,0xD3,0x00,0xDA,0x12,0xD5,0x80,0xD9,0xF1,0xDB,0x30,0x81,0xFF,0xA4,0xA6,0x8D,0x14,0xAF):
    cmd(c)
buf = bytearray(W * H // 8)
fb = framebuf.FrameBuffer(buf, W, H, framebuf.MONO_VLSB)
def show(l1, l2, l3):
    fb.fill(0)
    fb.text(l1, 0, 0, 1)
    fb.text(l2, 0, 24, 1)
    fb.text(l3, 0, 48, 1)
    cmd(0x21); cmd(0); cmd(W - 1); cmd(0x22); cmd(0); cmd(H // 8 - 1)
    i2c.writeto(ADDR, b"\x40" + buf)
btn = Pin(0, Pin.IN, Pin.PULL_UP)
print("idle level", btn.value())
show("BUTTON TEST", "idle: UP", "press BOOT")
t0 = None
fired = False
end = time.ticks_add(time.ticks_ms(), 30000)
print("READY, press BOOT now")
while time.ticks_diff(end, time.ticks_ms()) > 0:
    if btn.value() == 0:
        if t0 is None:
            t0 = time.ticks_ms()
            print("pressed")
        held = time.ticks_diff(time.ticks_ms(), t0)
        if held >= 3000 and not fired:
            fired = True
            print("HOLD 3s reached, portal would start")
            show("BUTTON TEST", "HOLD 3s", "PORTAL START")
        elif not fired:
            show("BUTTON TEST", "DOWN", str(held // 100 / 10) + " s")
    else:
        if t0 is not None:
            print("released after", time.ticks_diff(time.ticks_ms(), t0), "ms, portal fired:", fired)
            show("BUTTON TEST", "idle: UP", "press BOOT")
        t0 = None
        fired = False
    time.sleep_ms(20)
print("done")
"""

ser = serial.Serial()
ser.port = PORT
ser.baudrate = 115200
ser.timeout = 0.2
# Set these before open() so RTS never holds the board in reset.
ser.dtr = False
ser.rts = False
ser.open()
# Opening the port resets the board. Wait for it to boot and do not touch BOOT yet.
time.sleep(2.5)
ser.reset_input_buffer()
ser.write(b"\x03\x03")
time.sleep(0.3)
ser.write(b"\x05")
time.sleep(0.2)
for line in CODE.strip("\n").split("\n"):
    ser.write(line.encode() + b"\r")
    time.sleep(0.02)
ser.write(b"\x04")

deadline = time.time() + RUN_SECONDS
while time.time() < deadline:
    data = ser.read(256)
    if data:
        sys.stdout.write(data.decode(errors="replace"))
        sys.stdout.flush()
ser.close()
