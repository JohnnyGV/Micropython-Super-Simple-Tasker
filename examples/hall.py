from machine import Pin
import esp32

from sst import Sst
from vtc import Vtc

class Hall(object):

    
    def __init__(self, filter_len = 32):
        self.acc = 0
        self.task_id = Sst.add_task(self.hall_task)
        self.filter_len = filter_len

    def hall_task(self):
        self.acc -= self.acc // self.filter_len
        self.acc += esp32.hall_sensor()
        self.val = self.acc // self.filter_len
                    
    def hall_val(self):
        return self.val

h = Hall()
Vtc.add_timer(h.task_id, 20) # period (ms)   
Vtc.start_timers(1, 1) # timer_no, period




