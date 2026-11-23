from machine import UART, Pin
import time

uart = UART(
    1,
    baudrate=9600,
    bits=8,
    parity=None,
    stop=1,
    tx=Pin(6),
    rx=Pin(7),
    timeout=1000,
    timeout_char=50,
)


def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def request(addr):
    frame = bytes([addr, 0x04, 0x00, 0x00, 0x00, 0x0A])
    crc = crc16(frame)
    return frame + bytes([crc & 0xFF, crc >> 8])


def reg(data, i):
    return (data[2 * i] << 8) | data[2 * i + 1]


for n in range(5):
    uart.read()
    uart.write(request(0xF8))
    resp = uart.read(25)
    if resp is None:
        print(n, "no reply")
    elif len(resp) != 25:
        print(n, "short reply", resp.hex())
    else:
        crc = crc16(resp[:-2])
        if resp[-2] != (crc & 0xFF) or resp[-1] != (crc >> 8):
            print(n, "bad crc", resp.hex())
        else:
            d = resp[3:23]
            volts = reg(d, 0) / 10
            amps = (reg(d, 1) | (reg(d, 2) << 16)) / 1000
            watts = (reg(d, 3) | (reg(d, 4) << 16)) / 10
            wh = reg(d, 5) | (reg(d, 6) << 16)
            hz = reg(d, 7) / 10
            pf = reg(d, 8) / 100
            alarm = reg(d, 9)
            print(
                f"{n} ok V={volts} A={amps} W={watts} Wh={wh} Hz={hz} PF={pf} alarm={alarm}"
            )
    time.sleep(1)
