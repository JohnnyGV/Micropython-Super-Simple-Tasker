from machine import Pin
from machine import ADC

from sst import Sst
from vtc import Vtc

class Adc(object):
    def __init__(self, pin_no):
        self.adc = ADC(Pin(pin_no))
        self.task_id = Sst.add_task(self.adc_task)
        self.adcw = 0

    def adc_task(self):
        self.adcw = self.adc.read()

adc = Adc(32)
Vtc.add_timer(adc.task_id, 20) # period (ms)   
Vtc.start_timers(1, 1) # timer_no, period

 