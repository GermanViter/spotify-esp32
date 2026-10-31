import network
import env
import time


def connect(timeout=20):

    w = network.WLAN(network.STA_IF)
    w.active(True)

    if not w.isconnected():
        w.connect(env.SSID, env.WIFI_PASSWORD)
        t = 0

        while not w.isconnected() and t < 20:
            time.sleep(1)
            t += 1
    
    if not w.isconnected():
        raise OSError("wifi failed, status %d" % w.status())
    return w.ifconfig()

