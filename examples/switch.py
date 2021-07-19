#import micropython
#micropython.alloc_emergency_exception_buf(100)

from machine import Pin
from machine import Timer
import sst
from sst import Sst

class Switch(object): # example of simple state machine

    def __init__(self, pin_no, led_no):
        self.sw = Pin(pin_no, Pin.IN, Pin.PULL_UP)
        self.led = Pin(led_no, Pin.OUT)
        self.led.off()
        self.task_id = Sst.add_task(self.sw_task1) # initial state
        self.sw.irq(trigger=Pin.IRQ_RISING, handler = self.sw_cb)
        
    def sw_cb(self, pin):
        Sst.make_ready(self.task_id)
    
    def sw_task1(self): # led on & change state
        self.led.on()
        Sst.set_task(self.task_id, self.sw_task2)

    def sw_task2(self): # led off & change state
        self.led.off()
        Sst.set_task(self.task_id, self.sw_task1)

sw = Switch(0, 21) # switch pin, led pin
