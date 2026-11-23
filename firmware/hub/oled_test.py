from machine import Pin, I2C
import framebuf


class SSD1306(framebuf.FrameBuffer):
    def __init__(self, i2c, addr=0x3C, width=128, height=64):
        self.i2c = i2c
        self.addr = addr
        self.width = width
        self.height = height
        self.pages = height // 8
        self.buffer = bytearray(self.pages * width)
        super().__init__(self.buffer, width, height, framebuf.MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytes([0x80, cmd]))

    def init_display(self):
        for cmd in (
            0xAE,
            0x20,
            0x00,
            0x40,
            0xA1,
            0xA8,
            self.height - 1,
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
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def show(self):
        self.write_cmd(0x21)
        self.write_cmd(0)
        self.write_cmd(self.width - 1)
        self.write_cmd(0x22)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.i2c.writevto(self.addr, [b"\x40", self.buffer])


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306(i2c)

oled.fill(0)
oled.text("WATTLINK", 0, 0, 1)
oled.text("Hub OK", 0, 16, 1)
oled.rect(0, 30, 128, 34, 1)
oled.text("I2C 0x3C", 8, 42, 1)
oled.show()
print("oled done")
