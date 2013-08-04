import ctypes
from decimal import *


class DHT(object):
    """
    Wrapper for Adafruit DHT11/DHT22/AM2302 sensor Raspberry Pi driver.
    """
    def __init__(self, sensor, pin):
        """
        Initialize with sensor type as string and pin Raspberry Pi pin number as integer
        """
        self.DHTlib = ctypes.CDLL("./libAdafruit_DHT.so")
        if not self.DHTlib.init():
            raise IOError("Could not initialise BCM2835 - may need to run as root")
        self.sensor = self.DHTlib.parseType(ctypes.c_char_p(sensor))
        self.pin = ctypes.c_int(pin)
        self.DHTlib.readDHT.restype = ctypes.POINTER(ctypes.c_float)
    def read(self):
        """
        Returns a dict of decimals representing measured temperature and humidity
        """
        r = self.DHTlib.readDHT(self.sensor, self.pin, ctypes.c_int(0))
        if r[1] > 0:
            q = Decimal("0.1")
            return {"temp": Decimal(r[0]).quantize(q), "hum":Decimal(r[1]).quantize(q)}
        else:
            return False

