import pluto
import re
import serial.tools.list_ports
import gevent

class ArduinoUtil(object):
    """                                                                         
    A utility class containing all the Arduino-esque functions                  
    """
    @staticmethod
    def digitalWrite(board, pin_number, value):
        if isinstance(board, pluto.Board):
            board.digital[pin_number].write(value)
            
    @staticmethod
    def digitalRead(board, pin_number, value):
        if isinstance(board, pluto.Board):
            board.digital[pin_number].read()
        
    @staticmethod
    def blinkLED(board, pin_number=pluto.LED_BUILTIN, interval=1):
        if isinstance(board, Board):
            while True:
                board.digital[pin_number].write(HIGH)
                gevent.sleep(1)

class PortUtil(object):
    """Helper class that scan serial port automatically"""
    comports = [p[0] for p in serial.tools.list_ports.comports()]
    num_ports = len(comports)
    auto_port = None
    keywords = []
    patterns = []

    @classmethod
    def count_ports(cls):
        return cls.num_ports
    
    @classmethod
    def scan(cls, *args, **kwargs):
        if len(args) == 0:
            cls.keywords = ['usb', 'serial']
        else:
            for index, val in enumerate(args):
                cls.keywords.append(val)
                
        for keyword in cls.keywords:
            p = re.compile('(/dev/)((tty)|(cu)|.*).({0})\w*[\d]'.format(keyword))
            cls.patterns.append(p)

        for port in cls.comports:
            for pattern in cls.patterns:
                m = pattern.match(port)
                if m:
                    cls.auto_port = m.group()
                else:
                    pass

        return cls.auto_port


    