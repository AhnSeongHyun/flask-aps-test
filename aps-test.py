from gevent import monkey; monkey.patch_all()
from datetime import datetime, timedelta
import os
import time
from apscheduler.schedulers.gevent import GeventScheduler



def tick(scheduler):
    now = datetime.now()
    print('Tick! The time is: %s' % now)
    scheduler.add_job(tick2, 'date', next_run_time=datetime.now() + timedelta(seconds=5), args=(now,))

def tick2(now):
    print "ttt start : %s" % now
    time.sleep(10)
    print "ttt end : %s" % now


if __name__ == '__main__':
    scheduler = GeventScheduler()
    scheduler.add_job(tick, 'interval', seconds=3, args=(scheduler,))
    g = scheduler.start()  # g is the greenlet that runs the scheduler loop
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass