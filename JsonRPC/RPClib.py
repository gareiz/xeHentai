#!/usr/bin/env python
# -*- coding:utf-8 -*-
# JSON-RPC lib
# Contributor:
#      fffonion        <fffonion@gmail.com>
import json
import sys
import traceback
from Exception import *

rpc_version = 2.0
jsonrpc_illegal_call = ''

def JsonResponse(rpcid, result = None, errmsg = None):
    dic = {'id' : rpcid, 'jsonrpc' : rpc_version}
    if result:
        dic['result'] = result
    if errmsg:
        dic['error'] = {'message' : errmsg}
    return json.dumps(dic)

class JsonRpc():
    def __init__(self, methods = {}, rpcpath= '/jsonrpc'):
        self.methods = methods
        self.rpcpath = rpcpath
    
    def __call__(self, cmd):
        return self.call(cmd)
    
    def __getitem__(self, key):
        return self.methods[key]
    
    def __setitem__(self, key, value):
        self.methods[key] = value

    def __delitem__(self, key):
        del self.methods[key]
        
    def call(self, cmd):
        if 'id' not in cmd:
            rpcid = 0
        else:
            rpcid = cmd['id']
        if 'method' not in cmd or 'params' not in cmd:
            return JsonResponse(rpcid, errmsg = 'method or params not given')
        try:
            val = self.methods[cmd['method']](cmd['params'])
            return JsonResponse(rpcid, result = val)
        except:
            traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
            return JsonResponse(rpcid, errmsg = traceback_info)
        
    def install_method(self, method, func):
        if 'methods' not in self.__dict__:
            self.methods = {}
        if method in self.methods:
            raise JsonRPCException('method %s already installed' % method)
        else:
            self.methods[method] = func