import sys
import json
import display
import spotify
import wifi

oled = display.init_display()
display.show_text(oled, 'Hello World')

def run():
    print(wifi.connect())
    res = spotify.get_currently_playing()
    if sys.implementation.name == "micropython":
        print(res)
    else:
        print(json.dumps(res, indent=1))

if __name__ in ("__main__", "main"):
    run()
