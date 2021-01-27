class NTPtime():
    def __init__(self):
        return

    def NTPtime(self):
        try:
            import usocket as socket
        except:
            import socket
        try:
            import ustruct as struct
        except:
            import struct

        # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 3155673600

        # The NTP host can be configured at runtime
        # by doing: ntptime.host = 'myhost.org'
        host = "pool.ntp.org"

        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo(host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        return val - NTP_DELTA
