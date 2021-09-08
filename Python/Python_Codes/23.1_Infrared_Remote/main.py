from irrecvdata import irGetCMD
import sys
recvPin = irGetCMD(15)
try:
    while True:
        irValue = recvPin.ir_read()
        if irValue:
            print(irValue)
except Exception as ir_error:
    print('Error .......')
    sys.print_exception(ir_error)
    print('.......End of Error')














