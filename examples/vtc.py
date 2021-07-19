from machine import Timer

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

class Vtc(object): # uses class variables and class methods, don't try instantiate

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


 