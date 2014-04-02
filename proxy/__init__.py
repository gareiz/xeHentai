#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Proxy pool and proxy prototype
# Contributor:
#      fffonion        <fffonion@gmail.com>
import random

class Proxy:
    def __init__(self):
        self.enabled = True
        self.ip = None
        self.is_https = False
        self.whitelist = [ ]#regex url filter
    
    def handle_proxy(self):
        raise NotImplementedError("This method is empty")

    def test_proxy(self):
        raise NotImplementedError("This method is empty")

class ProxyPool:
    def __init__(self):
        self._pool = []
        self._forbidden_list = []
    
    def forbid(self, idx):
        if idx not in self._forbidden_list:
            self._forbidden_list.append(idx)
            
    def allow(self, idx):
        if idx in self._forbidden_list:
            del(self._forbidden_lis[self._forbidden_list.index(idx)])
        
    def put(self, proxy):
        if not isinstance(proxy, Proxy):
            raise TypeError("Input object is not a Proxy")
        else:
            self._pool.append(proxy)
        
    def get(self):
        if len(self._forbidden_list == self._pool):
            return None, None
        while True:
            idx = random.randrange(0, len(self._pool))
            if idx in self._forbidden_list:
                continue
            return idx, self._pool[idx]