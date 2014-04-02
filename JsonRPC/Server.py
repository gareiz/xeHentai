#!/usr/bin/env python
# -*- coding:utf-8 -*-
# JSON-RPC HTTP server
# Contributor:
#      fffonion        <fffonion@gmail.com>
import gzip
import socket
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from cStringIO import StringIO
from urlparse import urlparse
from Exception import *
import RPClib

__all__ = ['']

class HTTPServer(BaseHTTPRequestHandler, RPClib.JsonRpc):    
    def do(self, cmd):
        if urlparse(self.path).path != self.rpcpath:
            self.send_response(404)
            return
        response = self.call(json.dumps(cmd))
        self.send_response(200)
        self.send_header('Content-Type'.encode('ascii'), 'application/json-rpc'.encode('ascii'))
        self.headers['Host']
        try:
            assert('gzip' in self.headers['Accept-Encoding'])
            f = StringIO(response)
            gzipper = gzip.GzipFile(fileobj = f)
            response = gzipper.read()
        except:
            self.send_header('Content-Encoding'.encode('ascii'), 'indentity'.encode('ascii'))
        else:
            self.send_header('Content-Encoding'.encode('ascii'), 'gzip'.encode('ascii'))
        self.send_header('Content-Length'.encode('ascii'), len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def do_GET(self):
        self.do(self.kv2dict(self.path))
    
    def do_POST(self):
        self.do(self.rfile.read(int(self.headers['Content-Length'])))

    def kv2dict(self, url):
        query = urlparse(url).query
        return dict(map(lambda x: x.split('='), query.split('&')))

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET