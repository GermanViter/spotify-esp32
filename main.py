import sys
import json
import ssd1306
from machine import Pin, I2C
import spotify
import wifi
import config

i2c = I2C(scl=Pin(22), sda=Pin(21))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.text('Hello World', 0, 0)
oled.show()

def run():
    print(wifi.connect())
    res = spotify.get_currently_playing()
    if sys.implementation.name == "micropython":
        print(res)
    else:
        print(json.dumps(res, indent=1))

if __name__ in ("__main__", "main"):
    run()
    config.display()