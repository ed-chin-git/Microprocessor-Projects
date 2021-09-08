# On every boot (including wake-boot from deepsleep)
# boot.py is executed then main.py, then enters shell

# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()

# === CONNECT WiFi
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('dragon1', 'harveysucks2017')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

# === SET CLOCK ===
import ntptime
ntptime.settime() # set rtc to ntp

# === DISCONNECT Wifi ===
wlan.disconnect()

# === Print TIME ===
import time
year, month, day, hour, minute, second, weekday, yearday = time.localtime()  # Get RTC
print('Local time AFTER synchronization：{}-{}-{} {}:{}:{}'.format(int(month),day,year,hour,minute,second)) 

# === LIST FILES ===
import os
files=os.listdir()
if len(files)>0:
    print('This device has %d files'%len(files))
    for i in range(len(files)):
        print('file name:',files[i])
else:
    print("Device has no files!")