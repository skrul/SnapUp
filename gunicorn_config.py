import threading
from  apscheduler import scheduler

sched = scheduler.Scheduler()

bind = ['0.0.0.0:5000']
workers = 4


def some_job():
    print 'sched: ', threading.current_thread().name
    print 'some job executing...'


def when_ready(server):
    sched.start()
    sched.add_interval_job(some_job, seconds=2)
