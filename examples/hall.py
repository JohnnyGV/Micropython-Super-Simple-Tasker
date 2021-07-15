from machine import Pin
from machine import Timer
import esp32
import sst
from sst import Sst

class Hall(object):

    def __init__(self, timer_no, period, que_size):
        self.acc = 0
        self.timer = Timer(timer_no)
        self.task_id = Sst.add_task(self.hall_task, que_size)
        self.timer.init(period = period, mode = Timer.PERIODIC, callback = self.hall_cb)
        self.que_size = que_size

    def hall_cb(self, timer):
        for i in range(self.que_size):
            Sst.add_to_que(self.task_id, esp32.hall_sensor())
        Sst.make_ready(self.task_id)

    def hall_task(self, h):
        self.acc -= self.acc // self.que_size
        self.acc += h
        self.val = self.acc // self.que_size
                    
    def hall_val(self):
        return self.val

h = Hall(3, 300, 32) # timer no, period, deque length


