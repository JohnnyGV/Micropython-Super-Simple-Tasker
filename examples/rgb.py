from machine import Pin

from sst import Sst
from vtc import Vtc

class Rgb(object):
    def __init__(self, led_no):
        self.led = Pin(led_no, Pin.OUT)
        self.task_id = Sst.add_task(self.led_task)

    def led_task(self):
        self.led.value(not self.led.value())

red = Rgb(18) # pin no
green = Rgb(19)
blue = Rgb(23)
Vtc.add_timer(red.task_id, 200) # period (ms)   
Vtc.add_timer(green.task_id, 400)    
Vtc.add_timer(blue.task_id, 600)
Vtc.start_timers(1, 1) # timer_no, period

 