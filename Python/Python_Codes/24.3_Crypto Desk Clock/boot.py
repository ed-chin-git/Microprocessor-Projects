# On every boot (including wake-boot from deepsleep)
# boot.py is executed then main.py, then enters shell

# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()

# === CONNECT WiFi
import network
SS_ID = 'dragon1'
wlan_password = 'harveysucks2017'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(SS_ID, wlan_password) # ("geoffrey's eardrum", "password")
    while not wlan.isconnected():
        pass

print('network config:', wlan.ifconfig())

# # === DISCONNECT Wifi ===
# wlan.disconnect()

# === LIST FILES === 
import os
files=os.listdir()
if len(files)>0:
    print('This device has %d files'%len(files))
    for i in range(len(files)):
        print('file name:',files[i])
else:
    print("Device has no files!")