# Micropython-Super-Simple-Tasker

Loosely based on the work by Miro Samek and Robert Ward (https://github.com/KnightSch/sst)

An interesting backgrounder on SST: https://www.embedded.com/build-a-super-simple-tasker/

Developed on an ESP32 platform using webrepl and should work on other micropython platforms

Licensing
------------
See LICENSE file 

Description
-----------
This tasker allows up to 8 tasks. Tasks should be added in priority order using 'add_task' with highest priority task added first. Each task should be designed to run to completion. Scheduler is started using 'start'. Callback functions (for example from a timer or pin interrupts) may be used to wake up a task using 'make_ready'.

Simple state machines may implemented by using the initial state as the task. When the task is run, the state may be changed by setting the task for the next state using 'set_task'. See 'example.py" for a simple example.

ToDo
----
Add a mechanism to allow data from a callback (eg: from UART or ADC) to be passed to the task  

