# Micropython-Super-Simple-Tasker

Loosely based on the work by Miro Samek and Robert Ward (https://github.com/KnightSch/sst)

An interesting backgrounder on SST: https://www.embedded.com/build-a-super-simple-tasker/

Developed on an ESP32 platform using webrepl and should work on other micropython platforms

Licensing
------------
See LICENSE file 

Description
-----------
This tasker allows up to 16 tasks. Tasks should be added in priority order using 'add_task' with lowest priority task added first. Each task should be designed to run to completion. Each task may have an attached queue that may be used for passing information from another task or Callback function. Callback functions (for example from a timer or pin interrupts) may be used to wake up a task using 'make_ready'. The scheduler is started when the first 'make_ready' is called.

Simple state machines may implemented by using the initial state as the task. When the task is run, the state may be changed by setting the task for the next state using 'set_task'.

See examples directory for some simple examples.

ToDo
----
Add tasking primtives like mutex and semaphore
