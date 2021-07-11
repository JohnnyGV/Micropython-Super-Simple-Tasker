import log2
import machine

class Sst(object):

    tasks = [] # list of tasks, highest priority first
    current_priority = 255 # idle task, webrepl in this case
    ready_set = 0 # bit set of ready tasks
    
    @classmethod
    def add_task(cls, t): # tasks must be added in decreasing priority order up to 8 tasks
        if len(log2.log2_tab)==0:
            log2.init_log2()
        cls.tasks.append(t)
        return len(cls.tasks)-1

    @classmethod
    def set_task(cls, t, p): # change task at priority level
        cls.tasks[p] = t     # useful for implementing state machines        
                
    @classmethod
    def scheduler(cls, s):
        pin = cls.current_priority
        mask = 1
        prio = 0
        while cls.ready_set != 0:
            if log2.log2(cls.ready_set) < pin:
                cls.ready_set &= ~mask
                cls.current_prio = prio
                machine.enable_irq(s)
                cls.tasks[prio]()
                s=machine.disable_irq()
                mask = mask << 1
                prio += 1
            else:
                break                
        cls.current_priority = pin
        return s
        
    @classmethod
    def make_ready(cls, t):
        s=machine.disable_irq()
        cls.ready_set |= 2**t            
        s=Sst.scheduler(s)
        machine.enable_irq(s)
        
    @classmethod
    def start(cls):
        s=machine.disable_irq()
        s=Sst.scheduler(s)
        machine.enable_irq(s)
        