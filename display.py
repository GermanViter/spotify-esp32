from machine import Pin, I2C
import ssd1306

def init_display():
    i2c = I2C(scl=Pin(22), sda=Pin(21))
    return ssd1306.SSD1306_I2C(128, 64, i2c)

def show_text(oled, text):
    oled.fill(0)
    oled.text(text, 0, 0)
    oled.show()

def wrap_text(oled, text, x=0, y=0, max_chars=16, line_height=10):
    """Word-wrap text and display it on the OLED."""
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(current) + len(word) + (1 if current else 0) > max_chars:
            lines.append(current)
            current = word
        else:
            current = current + " " + word if current else word
    if current:
        lines.append(current)

    oled.fill(0)
    for i, line in enumerate(lines[:8]):  # max 8 lines on 64px display
        oled.text(line, x, y + i * line_height)
    oled.show() 

def display_progress(oled, progress_ms, duration_ms, x=10, y=49, width=108, height=5, onColor=1, ofColor=0):
    oled.fill_rect(x, y, width, height, ofColor)
    oled.rect(x, y, width, height, onColor)
    fill = int((width - 2) * progress_ms / duration_ms) if duration_ms else 0
    fill = max(0, min(fill, width - 2))
    oled.fill_rect(x + 1, y + 1, fill, height - 2, onColor)
    oled.show()
