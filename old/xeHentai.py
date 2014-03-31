  #!/usr/bin/python
# -*- coding:utf-8 -*-
# A multithread downloader for exhentai.org
# Contributor:
#      fffonion        <fffonion#gmail.com>

__version__ = 2.0

import urllib
import random
import threading
import re
import os, os.path as opth
import Queue
import time
import sys
import socket
import traceback
import locale
sys.path.insert(2, opth.join(opth.abspath('.'), 'dependency.zip'))
import httplib2
import convHans
import xeHentai_hath
import xeHentai_download
# import gzip,hmac
loginurl = 'http://e-hentai.org/bounce_login.php?b=d&bt=1-1'
baseurl = 'http://e-hentai.org'
myhomeurl = 'http://g.e-hentai.org/home.php'
cooid, coopw, cooproxy, self.ip_addr, THREAD_COUNT = '', '', '', '', 5
self.logged_in, OVERQUOTA, IS_REDIRECT = False, False, False
LAST_DOWNLOAD_SIZE = [0] * 5

class xeHentai():
    def __init__(self):
        pass

    @classmethod
    def parse_html(input, method):
        pass

    def 