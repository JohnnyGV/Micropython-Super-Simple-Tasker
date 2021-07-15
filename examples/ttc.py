from machine import Pin
from machine import Timer
from machine import ADC

from ucollections import OrderedDict
import sst
from sst import Sst

class Counter(object): # helper class
    
    def __init__(self, period):
        self.ctr = 0
        self.period = period
    
    def count(self):
        self.ctr += 1
        if self.ctr == self.period:
            self.ctr = 0;
            return True
        else:
            return False

# This class implements virtual periodic timers for tasks
# Overcomes the limitation on no of hardware timers (especially on ESP32)
# It uses 1 hardware timer with period as low as 1 mSec
# Virtual timer period is a multiple of the hardware timer period

class TT(object): # uses class variables and class methods, don't try instantiate

    counters = OrderedDict()
    timer = None
        
    @classmethod
    def start_timers(cls, timer_no, period):
        cls.timer = Timer(timer_no)
        cls.timer.init(period = period, mode = Timer.PERIODIC, callback = cls.tt_task)

    @classmethod
    def tt_task(cls, timer):
        for task_id, counter in cls.counters.items():
            if counter.count():
                Sst.make_ready(task_id)                
    
    @classmethod
    def add_timer(cls, task_id, period):
        cls.counters[task_id] = Counter(period)

class Foo(object):
    def __init__(self, led_no):
        self.led = Pin(led_no, Pin.OUT)
        self.task_id = Sst.add_task(self.led_task)

    def led_task(self):
        self.led.value(not self.led.value())

class Adc(object):
    def __init__(self, pin_no):
        self.adc = ADC(Pin(pin_no))
        self.task_id = Sst.add_task(self.adc_task)
        self.adcw = 0

    def adc_task(self):
        self.adcw = self.adc.read()

red = Foo(18) # pin no
green = Foo(19)
blue = Foo(23)
adc = Adc(32)
TT.add_timer(adc.task_id, 20) # period (ms)   
TT.add_timer(red.task_id, 200) # period (ms)   
TT.add_timer(green.task_id, 400)    
TT.add_timer(blue.task_id, 600)
TT.start_timers(1, 1)

 