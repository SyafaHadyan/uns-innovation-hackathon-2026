import sys
import time

import serial

PORT = sys.argv[2] if len(sys.argv) > 2 else "/dev/ttyUSB0"
BAUD = int(sys.argv[3]) if len(sys.argv) > 3 else 115200

with open(sys.argv[1], "rb") as f:
    lines = f.read().splitlines()

s = serial.Serial()
s.port = PORT
s.baudrate = BAUD
s.timeout = 0.1
s.dtr = False
s.rts = False
s.open()

# The Hub resets when the port opens, so wait for it to finish booting
time.sleep(3)
s.reset_input_buffer()

# Stop any running program, then enter paste mode
s.write(b"\x03\x03")
time.sleep(0.3)
s.write(b"\x05")
time.sleep(0.2)

for line in lines:
    s.write(line + b"\r\n")
    time.sleep(0.03)

# Ctrl-D runs the pasted code
s.write(b"\x04")

end = time.time() + 25
while time.time() < end:
    data = s.read(256)
    if data:
        print(data.decode(errors="replace"), end="", flush=True)

s.close()
