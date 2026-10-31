import wifi

try:
    print(wifi.connect())
except OSError as e:
    print("wifi:", e)
