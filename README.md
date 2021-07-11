# Micropython-Super-Simple-Tasker

Loosely based on the work by Miro Samek and Robert Ward (https://github.com/KnightSch/sst)

An interesting backgrounder on SST: https://www.embedded.com/build-a-super-simple-tasker/

Developed on an ESP32 platform using webrepl and should work on other micropython (or python) platforms

Licensing
------------
See LICENSE file 

Description
-----------

This tasker allows up to 8 tasks. Tasks should be added in priority order using 'add_task' with highest priority task added first. Each task should be designed to run to completion. Tasks can be readied for scheduling using 'make_ready'. Scheduler is started using 'start'.
