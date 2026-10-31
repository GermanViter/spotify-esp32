import sys
import json
# main.py -- put your code here!if __name__ in ("__main__", "main"):
import spotify
import wifi
import config
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