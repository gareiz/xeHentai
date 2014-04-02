#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Multi-threading pool
# Contributor:
#      fffonion        <fffonion@gmail.com>
from threading import Thread, RLock
from Queue import Queue, Empty
from time import sleep
import random
from Worker import Worker
from Job import Job
from Exception import *

class ThreadPool:
    def __init__(self, worker_demand = 5):
        self.worker_demand = worker_demand
        self._worker_lock = RLock()
        self._worker_count = 0
        self._active_count = 0
        self._jobs = Queue()
        self._is_dying = False
    
    def new_worker(self):
        with self._worker_lock:
            w = Worker(random.randint(1,self.worker_demand), self.get_job, self.post_active, self.post_dead)
            self._worker_count += 1
        w.start()
    
    def post_active(self, active):
        with self._worker_lock:
            if(active):
                self._active_count += 1
            else:
                self._active_count -= 1
                
    def post_dead(self):
        with self._worker_lock:
            self._worker_count -= 1
    
    def put_job(self, func, ret_func, *arg, **kwarg):
        if self._is_dying:
            return
        job = Job(func, ret_func, *arg, **kwarg)
        with self._worker_lock:
            self._jobs.put(job)
            if self._worker_count < self.worker_demand and \
                self._active_count == self._worker_count:
                self.new_worker()
    
    def get_job(self):
        try:
            if (self._is_dying == 0):
                job = self._jobs.get(False)
            elif (self._is_dying == 0):
                job = self._jobs.get(True)
            #else:
            #    job = self.__jobs.get(True, self.__kill_workers_after)
        except Empty:
            job = None
        return job

    def shutdown(self,retries = 5, wait_interval = 5):        
        with self._worker_lock:
            self._is_dying = True
            self.worker_demand = 0 #no more new birth
            
        retries_left = retries
        while (retries_left > 0):
            with self._worker_lock:
                if (self._worker_count > 0):
                    retries_left -= 1
                else:
                    retries_left = 0
            sleep(wait_interval)
        
        with self.__worker_count_lock:
            if (self._worker_count > 0):
                dirty = False
            else:
                dirty = True

        return dirty

if __name__ == '__main__':
    def p(a, b = 2):
        print 'sleep'
        sleep(1)
        print('%d,%d' % (a, b))
        return i
    def q(a):
        print(str(a) + ' done')
    tp = ThreadPool(5)
    for i in range(10):
        tp.put_job(p, q, i, b=i*2)
    print 'wait for output'
    