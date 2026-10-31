from machine import Pin, I2C
import ssd1306

def init_display():
    i2c = I2C(scl=Pin(22), sda=Pin(21))
    return ssd1306.SSD1306_I2C(128, 64, i2c)

def show_text(oled, text):
    oled.fill(0)
    oled.text(text, 0, 0)
    oled.show()