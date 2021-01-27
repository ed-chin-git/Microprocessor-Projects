from time import sleep_ms
from machine import Pin

led1=Pin(2,Pin.OUT) #create LED object from pin2,Set Pin2 to output
led2=Pin(4,Pin.OUT) #create LED object from pin4,Set Pin4 to output
led3=Pin(5,Pin.OUT) #create LED object from pin4,Set Pin4 to output

led1.value(1)      
led2.value(1)   
led3.value(1)  
try:
    while True:
        led1.value(0) 
        led2.value(0) 
        led3.value(0) 
        sleep_ms(200)
        led1.value(1) 
        sleep_ms(300)
        led2.value(1)
        sleep_ms(400)
        led3.value(1)
        sleep_ms(500)
except:
    pass





