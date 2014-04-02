#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Exception definations
# Contributor:
#      fffonion        <fffonion@gmail.com>

class ThreadPoolException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)