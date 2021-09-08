# https://techtutorialsx.com/2017/06/11/esp32-esp8266-micropython-http-get-requests/
import time
import ntptime
from machine import I2C, Pin, PWM
from I2C_LCD import I2cLcd
import dht
import urequests as requests
import sys
import network
wlan = network.WLAN(network.STA_IF)

# === set time to ntp
ntptime.settime() # set rtc to ntp
# === Print TIME to terminal ===
year, month, day, hour, minute, second, weekday, yearday = time.localtime()  # Get RTC
print('Local UTC time AFTER synchronization：{}-{}-{} {}:{}:{}'.format(int(month),day,year,hour,minute,second)) 

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

# === config LCD panel ===
DEFAULT_I2C_ADDR = 0x27
i2c = I2C(scl=Pin(14),
          sda=Pin(13),
          freq=400000) # assign pins

lcd = I2cLcd(i2c,
             DEFAULT_I2C_ADDR,
             2,
             16) # instantiate object

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr(wlan.config('essid'))

lcd.move_to(0, 1)
ip_addr, sub_net, gate_way, dns_serv = wlan.ifconfig()
lcd.putstr(ip_addr)

# === Define custom LCD character ===
degree_chr = bytearray([0b11110,
                        0b10010,
                        0b10010,
                        0b11110,
                        0b00000,
                        0b00000,
                        0b00000,
                        0b00000])
# assign to chr(1) (1-7 are available)
lcd.custom_char(1, degree_chr) 

# === Define Conversion tables ===
#     24-->12hr & day-of-week
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

## timezone offset in hours
year, month, day, hour, minute, second, weekday, yearday = time.localtime()
if (month > 2 ) and (month < 11) :
    offset_hrs = -5  ## Daylight savings from Mar 14 to Nov 7 (Spring fwd)
else:
    offset_hrs = -6  ## (Fall back)

# == initialize work variables ===
eth_usd_price = "0000.00"
btc_usd_price = "0000.00"
ada_usd_price = "0000.00"
dot_usd_price = "0000.00"
xrp_usd_price = "0000.00"
xag_usd_price = "0000.00"
sol_usd_price = "0000.00"
strong_usd_price = "0000.00"


metalsAPI_url_prefix = 'https://www.goldapi.io/api'
metalsAPI_headers = {'x-access-token' : 'goldapi-7m13uiukl1awd22-io',
                   'Content-Type': 'application/json'}

j = 0  # joke-index
last_updated = 0
metals_last_updated = 0

# === MAIN LOOP ===
# (approx 1 loop per minute) 
while True:
    # === Get RTC system time
    systime = time.mktime(time.localtime())
    year, month, day, hour, minute, second, weekday, yearday = time.localtime()
    if (year == 1999  ) and (month == 12) and (day == 31) :
        ntptime.settime() # set rtc to ntp
        systime = time.mktime(time.localtime())
        if (month > 2 ) and (month < 11) :
            offset_hrs = -5  ## Daylight savings from Mar 14 to Nov 7 (Spring fwd)
        else:
            offset_hrs = -6;  ## (Fall back) 

    # === Get Metal prices
    # ===   every 1.75-hrs / 105-mins / 6300-secs
    if (metals_last_updated == 0) | ( systime > (metals_last_updated + 6300)):
        metals_last_updated = time.mktime(time.localtime())
        # === Get XAG_USD price
        try:
            resp = requests.get( str(metalsAPI_url_prefix + '/XAG/USD/'),
                                headers=metalsAPI_headers)
            if resp.status_code == 200:
                response_dict = resp.json()
                xag_usd = response_dict["price"]
                xag_usd_price = xag_usd
            else:
                print(resp.status_code)
        except Exception as xag_error:
            sys.print_exception(xag_error)
            xag_usd_price = "ERROR"
        # === Get XAU_USD price
        try:
            resp = requests.get( str(metalsAPI_url_prefix + '/XAU/USD/'),
                                headers=metalsAPI_headers)
            if resp.status_code == 200:
                response_dict = resp.json()
                xau_usd = response_dict["price"]
                xau_usd_price = xau_usd
            else:
                print(resp.status_code)
        except Exception as xau_error:
            sys.print_exception(xau_error)
            xau_usd_price = "ERROR"

    # === Get crypto prices every 5 minutes
    if (last_updated == 0) | ( systime > (last_updated + 300)):
        last_updated = time.mktime(time.localtime())
        # === Get BTC price
        try:
            #== alternative source -> https://api.coindesk.com/v1/bpi/currentprice.json
            resp = requests.get('https://api.cryptonator.com/api/ticker/btc-usd')
            if resp.status_code == 200:
                response_dict = resp.json()
                usd = response_dict["ticker"]
                btc_usd = usd["price"]
                btc_usd_price = btc_usd.split('.')
            else:
                btc_usd_price = 0.0000
                print(resp.status_code)
        except Exception as btc_error:
            sys.print_exception(btc_error)
            btc_usd_price = "ERROR"
        # === Get ETH price
        try:
            resp = requests.get('https://api.cryptonator.com/api/ticker/eth-usd')
            if resp.status_code == 200:
                response_dict = resp.json()
                usd = response_dict["ticker"]
                eth_usd = usd["price"]
                eth_usd_price = eth_usd.split('.')[0]
            else:
                print(resp.status_code)
        except Exception as eth_error:
            sys.print_exception(eth_error)
            eth_usd_price = "ERROR"
        # === Get XRP price
        try:
            resp = requests.get('https://api.cryptonator.com/api/ticker/xrp-usd')
            if resp.status_code == 200:
                response_dict = resp.json()
                usd = response_dict["ticker"]
                xrp_usd = usd["price"]
                xrp_usd_price = float(xrp_usd)
            else:
                print(resp.status_code)
        except Exception as xrp_error:
            sys.print_exception(xrp_error)
            xrp_usd_price = "ERROR"
        # === Get ADA price
        try:
            resp = requests.get('https://api.cryptonator.com/api/ticker/ada-usd')
            if resp.status_code == 200:
                response_dict = resp.json()
                usd = response_dict["ticker"]
                ada_usd = usd["price"]
                ada_usd_price = float(ada_usd)
            else:
                print(resp.status_code)
        except Exception as ada_error:
            sys.print_exception(ada_error)
            ada_usd_price = "ERROR"        
     # === Get DOT price
        try:
            resp = requests.get('https://api.cryptonator.com/api/ticker/dot-usd')
            if resp.status_code == 200:
                response_dict = resp.json()
                usd = response_dict["ticker"]
                dot_usd = usd["price"]
                dot_usd_price = float(dot_usd)
            else:
                print(resp.status_code)
        except Exception as dot_error:
            sys.print_exception(dot_error)
            dot_usd_price = "ERROR"
            
     # === Get sol price
        try:
            resp = requests.get('https://api.cryptonator.com/api/ticker/sol-usd')
            if resp.status_code == 200:
                response_dict = resp.json()
                usd = response_dict["ticker"]
                sol_usd = usd["price"]
                sol_usd_price = float(sol_usd)
            else:
                print(resp.status_code)
        except Exception as sol_error:
            sys.print_exception(sol_error)
            sol_usd_price = "ERROR"
     
     # === Get strong price
        try:
            resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=strong&vs_currencies=usd')
            if resp.status_code == 200:
                response_dict = resp.json()
                usd = response_dict["strong"]
                strong_usd = usd["usd"]
                strong_usd_price = float(strong_usd)
            else:
                print(resp.status_code)
        except Exception as strong_error:
            sys.print_exception(strong_error)
            strong_usd_price = "ERROR"
                   
            
    # === Flip btwn time & crypt-prices // 4 loops * 15 secs = (60 secs)
    for t in range(0,4):
        # === Get RTC system time
        systime = time.mktime(time.localtime())
        # === Convert to current timezone offset
        disp_time = systime + ((offset_hrs*60) * 60)
        year, month, day, hr24, minute, second, weekday, yearday = time.localtime(disp_time)
        # === Convert to 12hr format
        hr12 = cnv_2412[hr24]

        # === Time/Temp Screen        
        lcd.clear()
        # === Display Day of week === 
        lcd.move_to(0, 1)
        day_wk = day_of_week[weekday]
        lcd.putstr('{}'.format(day_wk))
        # === Display Date ===
        lcd.move_to(0, 0)
        lcd.putstr('{:02d}-{:02d}-{}'.format(month,day,str(year)[2:5])) 
        # === Display Time ===
        lcd.move_to(9, 0)
        lcd.putstr('{}:{:02d}{}'.format(hr12[0:2],minute,hr12[2:5]))
        # === Get Temp/humidity ===
        try:
            DHT.measure()
            Ftemp = round((DHT.temperature() * 9) / 5) + 32
            Humid = DHT.humidity()
        except:
            Ftemp = 999
            Humid = 999
        # === Display Temp/humidity ===
        if Ftemp < 999:
            lcd.move_to(7, 1)
            lcd.putstr(str(Ftemp)+' F '+str(Humid)+"%h")
            lcd.move_to(9, 1)
            lcd.putstr(str(chr(1))) # print custom degree char
        time.sleep_ms(3000)

        # === Price Screen 1 ===
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('BTC:'+'{:,}'.format(int(btc_usd_price[0])))
        # === Display ETH price
        if eth_usd_price != "0000.00":
            lcd.move_to(0,1) 
            lcd.putstr('ETH:'+'{:,}'.format(int(eth_usd_price)))
        time.sleep_ms(3000)

        # === Price Screen 2 ===
        lcd.clear()
        lcd.move_to(0, 0) 
        # === Display ADA price
        if ada_usd_price != "0000.00":
            lcd.putstr('ADA:'+'{:.4f}'.format(ada_usd_price))
        lcd.move_to(0, 1)
        # === Display DOT price
        if dot_usd_price != "0000.00":
            lcd.putstr('DOT:'+'{:.4f}'.format(dot_usd_price))
        
        time.sleep_ms(3000)
        
        # === Price Screen 3 ===
        lcd.clear()
        # === Display sol price ===
        if sol_usd_price != "0000.00":
            lcd.move_to(0, 0)
            lcd.putstr('SOL:'+'{:.4f}'.format(sol_usd_price))
        # === Display strong price ===
        if strong_usd_price != "0000.00":
            lcd.move_to(0, 1)
            lcd.putstr('STRONG:'+'{:.2f}'.format(strong_usd_price))        

#         # === Display XRP price ===
#         if xrp_usd_price != "0000.00":
#             lcd.move_to(0, 1)
#             lcd.putstr('XRP:'+'{:.4f}'.format(xrp_usd_price))
        time.sleep_ms(3000)
        
        # === Price Screen 4 ===
        lcd.clear()
        # === Display Silver price ===
        lcd.move_to(0, 0)
        if xag_usd_price != "0000.00":
            lcd.putstr('XAG:'+'{:.2f}'.format(xag_usd_price))
        # === Display Gold price ===
        lcd.move_to(0, 1)
        if xag_usd_price != "0000.00":
            lcd.putstr('XAU:'+'{:.2f}'.format(xau_usd_price))
        time.sleep_ms(3000)
        
    # === Display next joke ===
    joke1, joke2, answer = jokes[j]
    lcd.clear()
    lcd.putstr(joke1)
    time.sleep_ms(4000)
    lcd.clear()
    lcd.putstr(joke2)
    time.sleep_ms(4000)
    lcd.clear()
    lcd.putstr(answer)
    time.sleep_ms(5500)
    j += 1   # increment joke counter
    if j > (len(jokes)-1):
        j = 0 # Reset the counter
