#import micropython
#micropython.alloc_emergency_exception_buf(100)

from machine import Pin
from machine import Timer
import sst
from sst import Sst

class Foo(object):
    def __init__(self, timer_no, period, led_no):
        self.led = Pin(led_no, Pin.OUT)
        self.timer = Timer(timer_no)
        self.task = 0
        self.timer.init(period=period, mode=Timer.PERIODIC, callback=self.cb)
        self.task_id = Sst.add_task(self.led_on_task)
        
    def cb(self, timer):
        Sst.make_ready(self.task_id)

    def led_on_task(self):
        self.led.on()
        Sst.set_task(self.led_off_task, self.task_id)

    def led_off_task(self):
        self.led.off()
        Sst.set_task(self.led_on_task, self.task_id)

def run():
    red = Foo(1, 197, 18) 
    green = Foo(2, 167, 19)
    blue = Foo(3, 143, 23)
    Sst.start()
 
run()
