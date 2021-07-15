import machine
from ucollections import deque

class Sst(object): # uses class variables and class methods, don't try instantiate

    log2_tab = ( \
        0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, \
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, \
        6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, \
        6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, \
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, \
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, \
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, \
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, \
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8)

    tasks = [] # list of tasks, lowest priority first
    current_priority = -1 # idle task, (web)repl in this case
    ready_set = 0 # bit set of ready tasks
    params = [] # parameter to task

    @classmethod
    def log2(cls, i): # helper function
        if i < 256:
            return cls.log2_tab[i] - 1
        else:
            return cls.log2_tab[i >> 8] + 7
    
    @classmethod
    def mask(cls, i): # helper function
        MASK = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768)
        return MASK[i]
        
    @classmethod
    def add_task(cls, task, deque_size = 0): # tasks will be added in increasing priority order up to 16 tasks
        s = machine.disable_irq()
        cls.tasks.append(task)
        if deque_size != 0:
            cls.params.append(deque((), deque_size))
        else:
            cls.params.append(None)
        id = len(cls.tasks)-1 # this is used as task id
        machine.enable_irq(s)
        return id

    @classmethod
    def set_task(cls, task, task_id):  # useful for implementing state machines
        s=machine.disable_irq()
        cls.tasks[task_id] = task        
        machine.enable_irq(s)
                
    @classmethod
    def scheduler(cls, s): # runs the highest priority task
        pin = cls.current_priority
        while cls.ready_set != 0:
            prio = cls.log2(cls.ready_set) # uses int log2 to find highest priority task
            if prio > pin:
                cls.current_prio = prio
                f = cls.tasks[prio]
                q = cls.params[prio]
                if q == None:
                    cls.ready_set &= ~cls.mask(prio)
                    machine.enable_irq(s)
                    f()
                    s = machine.disable_irq()
                else:
                    p = q.popleft()
                    if len(q) == 0:
                        cls.ready_set &= ~cls.mask(prio)
                    machine.enable_irq(s)
                    f(p)
                    s = machine.disable_irq()
            else:
                break                
        cls.current_priority = pin
        return s
        
    @classmethod
    def make_ready(cls, task_id): # makes task ready and schedules it to run
        s = machine.disable_irq()
        cls.ready_set |= cls.mask(task_id)
        s = cls.scheduler(s)
        machine.enable_irq(s)

    @classmethod
    def add_to_que(cls, task_id, val): # add an item to task deque, typically used by callback
        s = machine.disable_irq()
        cls.params[task_id].append(val)
        machine.enable_irq(s)

    @classmethod
    def post_to_que(cls, task_id, val): # add an item to task deque, make it ready and call scheduler
        s = machine.disable_irq()
        cls.params[task_id].append(val)
        cls.ready_set |= cls.mask(task_id)
        s = cls.scheduler(s)
        machine.enable_irq(s)

    @classmethod
    def replace_task(cls, task_id, task, deque_size = 0): # replaces a task
        s = machine.disable_irq()
        tasks[task_id] = task
        if deque_size == 0:
            params[task_id] = None
        else:
            params[task_id] = deque((), deque_size)
        machine.enable_irq(s)

    