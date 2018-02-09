#coding=utf-8
import time
import sched
import datetime,os,platform
def timerFun(sched_Timer):
    flag = 0
    while True:
        now = datetime.datetime.now()
        if now == sched_Timer:
            test()
            flag = 1
        else:
            if flag == 1:
                sched_Timer = sched_Timer+datetime.timedelta(minutes=1)
                flag=0

def test():
    time_from = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 86400))
    time_to = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print time_from + "url" + time_to
if __name__ == '__main__':
    sched_Timer = datetime.datetime(2017,11,2,9,30)
    print 'run the time task at {0}'.format(sched_Timer)
    timerFun(sched_Timer)

