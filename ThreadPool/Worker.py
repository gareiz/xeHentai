#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Worker, a single thread
# Contributor:
#      fffonion        <fffonion@gmail.com>
from threading import Thread

class Worker(Thread):
    def __init__(self, name, get_job_func, set_active_func, dead_func, logger = None):
        Thread.__init__(self, name = name)
        self.name = name
        self.get_job_func = get_job_func
        self.set_active_func = set_active_func
        self.dead_func = dead_func
        self.alive = True
        if logger:
            self.logger = lambda x : logger('%s - %s' % (self.name, x))
        else:
            self.logger  = lambda x : x
    
    def run(self):
        while self.alive:
            job = self.get_job_func()
            if(not job):
                break
            self.set_active_func(True)
            try:
                job.do()
            except Exception as e:
                self.logger('Encounted an error:%s' % e)
            self.set_active_func(False)

        self.dead_func()