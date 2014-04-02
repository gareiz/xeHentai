import unittest
from Proxy.glype import glype

class ProxyTest(unittest.TestCase):
    def setUp(self):
        pass

    def testGlype(self):
        g1 = glype('http://t.c/yoo.php?s=q&b=1&u=231')
        g2 = glype('http://t.c/yoo.php?b=1&u=231&s=q')
        cases = [('www.baidu.com', 'http://t.c/yoo.php?b=1&u=www.baidu.com&s=q'),
                 ('http://www.baidu.com', 'http://t.c/yoo.php?b=1&u=http%3A%2F%2Fwww.baidu.com&s=q'),
                 ('http://t.c/yoo.php?b=1&u=haha.com&s=q', 'http://t.c/yoo.php?b=1&u=haha.com&s=q'),]
        for (u,v) in cases:
            self.assertEqual(g1.handle_proxy(u), v)
            self.assertEqual(g2.handle_proxy(u), v)
        g1.whitelist=['.*haha\.com']
        self.assertEqual(g1.handle_proxy('v.haha.com'), 'v.haha.com')
        self.assertEqual(g1.handle_proxy('whatever.com'), 'http://t.c/yoo.php?b=1&u=whatever.com&s=q')
            

if __name__ == '__main__':
    ProxyTest.main()