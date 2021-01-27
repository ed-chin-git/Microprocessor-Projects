from time import sleep_ms
from machine import I2C, Pin
from I2C_LCD import I2cLcd
import dht

DHT = dht.DHT11(Pin(18))

# CONFIG LCD PANEL
# Custom Character Generator
# for HD44780 LCD Modules
# https://omerk.github.io/lcdchargen/
DEFAULT_I2C_ADDR = 0x27
i2c = I2C(scl=Pin(14), sda=Pin(13), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

try:
    while True:
        lcd.move_to(0, 0)

        DHT.measure()
        Ftemp = round((DHT.temperature() * 9) / 5) + 32
        lcd.putstr("Temp: ")
        lcd.putstr(str(Ftemp)+'f / ')
        lcd.putstr(str(DHT.temperature())+'c')

        lcd.move_to(0, 1)
        lcd.putstr(  "Humidity: "+str(DHT.humidity())+"%")
        sleep_ms(1000)
except:
    pass