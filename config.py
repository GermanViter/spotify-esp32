from machine import Pin, I2C
import ssd1306

def display():
    i2c = I2C(scl=Pin(22), sda=Pin(21))

    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

    oled.text('Hello World', 0, 0)
    oled.show()