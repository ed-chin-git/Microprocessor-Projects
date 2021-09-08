from irrecvdata import irGetCMD
import sys

recvPin = irGetCMD(15)
try:
    while True:
        print('in')
        irValue = recvPin.ir_read()
        print('out')
        if irValue:
            print(irValue)
except:
    print(sys.exc_info()[0], 'occurred.')















