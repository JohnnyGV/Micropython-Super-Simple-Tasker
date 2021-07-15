#import micropython
#micropython.alloc_emergency_exception_buf(100)

from machine import Pin
from machine import Timer
import sst
from sst import Sst

class Switch(object):
    sw = None
    task_id = 0
    led = None
    def __init__(self, pin_no, led_no):
        self.sw = Pin(pin_no, Pin.IN, Pin.PULL_UP)
        self.led = Pin(led_no, Pin.OUT)
        self.task_id = Sst.add_task(self.sw_task)
        self.sw.irq(trigger=Pin.IRQ_RISING, handler = lambda t: Sst.make_ready(self.task_id))
        
    def sw_task(self): # toggle led
        self.led.value(not self.led.value())

sw = Switch(0, 21) # switch pin, led pin
