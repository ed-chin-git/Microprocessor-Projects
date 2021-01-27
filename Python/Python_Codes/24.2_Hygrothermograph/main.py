# https://techtutorialsx.com/2017/06/11/esp32-esp8266-micropython-http-get-requests/
import time
from machine import I2C, Pin
from I2C_LCD import I2cLcd
import dht
import urequests as requests

# === Load joke file
jokes = []
jokefile = open("jokefile.txt", "r")
for line in jokefile:
    values = line.split(',')  
    item = (values[0], values[1], values[2])
    jokes.append(item)
jokefile.close()

# === config temp sensor
DHT = dht.DHT11(Pin(18))

# === config LCD panel
DEFAULT_I2C_ADDR = 0x27
i2c = I2C(scl=Pin(14),
          sda=Pin(13),
          freq=400000) # assign pins
lcd = I2cLcd(i2c,
             DEFAULT_I2C_ADDR,
             2,
             16) # instantiate object

# === Define custom LCD character
degree_chr = bytearray([0b11110,
                        0b10010,
                        0b10010,
                        0b11110,
                        0b00000,
                        0b00000,
                        0b00000,
                        0b00000])
lcd.custom_char(1, degree_chr) # assign to chr(1) (1-7 are available)

# === 24hour conversion table
cnv_2412 =  {0:'12am',
             1:' 1am',
             2:' 2am',
             3:' 3am',
             4:' 4am',
             5:' 5am',
             6:' 6am',
             7:' 7am',
             8:' 8am',
             9:' 9am',  
            10:'10am',
            11:'11am',
            12:'12pm',
            13:" 1pm",
            14:" 2pm",
            15:" 3pm",
            16:" 4pm",
            17:" 5pm",
            18:" 6pm",
            19:" 7pm",
            20:" 8pm",
            21:" 9pm",
            22:"10pm",
            23:"11pm"}
 
day_of_week =  {0:'Mon',
                1:'Tue',
                2:'Wed',
                3:'Thu',
                4:'Fri',
                5:'Sat',
                6:'Sun'}               

offset_hrs = -6  # timezone offset in hours

# === MAIN LOOP
j = 0
try:
    while True:
        lcd.clear()

        # === Get RTC system time
        systime = time.mktime(time.localtime())
        
        # === Convert to current timezone offset
        disp_time = systime + ((offset_hrs*60) * 60)
        year, month, day, hour, minute, second, weekday, yearday = time.localtime(disp_time)

        # === Convert to 12hr format
        tz12 = cnv_2412[hour]
        
        # === Display Day of week
        lcd.move_to(0, 1)
        day_wk = day_of_week[weekday]
        lcd.putstr('{}'.format(day_wk))

        # === Display Date
        lcd.move_to(0, 0)
        lcd.putstr('{:02d}-{:02d}-{}'.format(month,day,str(year)[2:5])) 

        # === Display Time
        lcd.move_to(9, 0)
        lcd.putstr('{}:{:02d}{}'.format(tz12[0:2],minute,tz12[2:5]))

        # === Get Temp/humidity
        DHT.measure()
        Ftemp = round((DHT.temperature() * 9) / 5) + 32

        # === Display Temp/humidity
        lcd.move_to(7, 1)
        lcd.putstr(str(Ftemp)+' F '+str(DHT.humidity())+"%h")
        lcd.move_to(9, 1)
        lcd.putstr(str(chr(1))) # print custom degree char
        time.sleep_ms(42000)
        
        # === Access Coindesk API
        try:  
            response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
            response_dict = response.json()
            bpi=response_dict["bpi"]
            usd=bpi["USD"]
            btc_usd_price = usd["rate"][:6]
        except:
            print(response.status_code)
            print(response.reason)
            btc_usd_price = "ERROR"

        # === Display BTC price
        lcd.clear()
        lcd.putstr('BTC/USD= '+btc_usd_price)
        time.sleep_ms(7000)

        # === Display next joke
        joke1, joke2, answer = jokes[j]
        lcd.clear()
        lcd.putstr(joke1)
        time.sleep_ms(3000)
        lcd.clear()
        lcd.putstr(joke2)
        time.sleep_ms(4000)
        lcd.clear()
        lcd.putstr(answer)
        time.sleep_ms(4000)
        j = j+1   # increment joke counter
        if j > (len(jokes)-1):
            j = 0
except:
    print('Fatal error...  could not start main loop')