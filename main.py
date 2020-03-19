import webrepl
import wifi_scan
webrepl.start()

display = wifi_scan.WiFiScanner(5, 4)
while True:
    display.format()

print(display)
