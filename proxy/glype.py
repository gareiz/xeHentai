#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Glype Porxy handler
# Contributor:
#      fffonion        <fffonion@gmail.com>
import re
import urllib
from __init__ import Proxy

class glype(Proxy):
    def __init__(self, base, crypt_url = False):
        Proxy.__init__(self)
        self.base = base
        self.crypt_url = crypt_url
        self.gen_lambda()

    def handle_proxy(self, url):
        if url.find(self._server) != -1:
            return url
        for f in self.whitelist:
            if re.search(f, url):
                return url
        if self.crypt_url:
            raise NotImplementedError
        else:
            return self._go(urllib.quote_plus(url))

    def gen_lambda(self):
        if self.base.startswith('https://'):
            self.is_https = True
        _find = re.findall('^http[s]*://([^/]+)/([^\?]+)\?', self.base)
        _cfg = re.findall('\?.*?(\w+)=(\d+)[&|$]', self.base)
        if not _find or not _cfg:
            raise ValueError('Cannot parse Porxy path.')
        self._server, self._script = _find[0]
        self._cfg_arg, self._cfg_value = _cfg[0]
        args = re.findall('(\w+)=([^&]+)', self.base)
        self._other_arg = '&'.join(['%s=%s' % (i,j) for i,j in args if i not in [self._cfg_arg, 'u']])
        self._go = lambda x : '%s://%s/%s?%s=%s&u=%s&%s' %(
                    self.is_https and 'https' or 'http',
                    self._server, self._script,
                    self._cfg_arg, self._cfg_value,
                    x, self._other_arg)
        

    def test_proxy(self):
        pass

if __name__ == '__main__':
    g=glype('http://t.c/yoo.php?b=1&u=231&norefer=1')