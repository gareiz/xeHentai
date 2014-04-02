#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Wrapping job
# Contributor:
#      fffonion        <fffonion@gmail.com>

class Job():
    def __init__(self, func, ret_func, *arg, **kwarg):
        self.func = func
        self.arg = arg
        self.kwarg = kwarg
        self.ret_func = ret_func
    
    def do(self):
        val = self.func(*self.arg, **self.kwarg)
        self.ret_func(val)