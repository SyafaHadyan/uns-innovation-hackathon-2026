# WATTLINK Plug simulated overload cutoff test
# Board is ESP32-C3 SuperMini running MicroPython. No mains and no load.
# Relay S pin is on GPIO3 and is active HIGH. HIGH closes the contact and LOW opens it.
# The wattage values below are fake. The PZEM is not read in this test.

import time
from machine import Pin

RELAY_PIN = 3
LIMIT_W = 2200.0
STEP_MS = 1500
SEQUENCE = [0.0, 5.0, 120.0, 800.0, 1500.0, 2100.0, 2199.0, 2201.0, 2400.0, 800.0]

relay = Pin(RELAY_PIN, Pin.OUT, value=0)


def classify(p, closed):
    if p > LIMIT_W:
        return 3
    if closed and 1.2 < p < 8.5:
        return 1
    return 0


print("TEST simulated overload cutoff")
print("LIMIT_W", LIMIT_W, "RELAY_PIN", RELAY_PIN)
time.sleep_ms(1000)
relay.value(1)
print("relay closed at start, state", relay.value())
time.sleep_ms(STEP_MS)

first_over = None
opened_at = None
open_ms = None
early_open = False
reopened = False

for i, p in enumerate(SEQUENCE):
    t0 = time.ticks_us()
    closed = relay.value() == 1
    status = classify(p, closed)
    if status == 3 and closed:
        relay.value(0)
        open_ms = time.ticks_diff(time.ticks_us(), t0) / 1000.0
        opened_at = i
    if p > LIMIT_W and first_over is None:
        first_over = i
    if p <= LIMIT_W and relay.value() == 0 and opened_at is None:
        early_open = True
    if opened_at is not None and i > opened_at and relay.value() == 1:
        reopened = True
    print("sample", i, "P_fake_W", p, "status", status, "relay", relay.value())
    time.sleep_ms(STEP_MS)

ok = (
    first_over is not None
    and opened_at == first_over
    and not early_open
    and not reopened
    and relay.value() == 0
)
print("first sample over limit", first_over)
print("relay opened at sample", opened_at)
print("time from sample to relay open ms", open_ms)
print("relay final state", relay.value())
print("RESULT", "PASS" if ok else "FAIL")
