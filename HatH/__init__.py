#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
# A file parser for h@h(.hathdl)
# Contributor:
#      fffonion        <fffonion@gmail.com>

__version__ = 1.1
import re
import math
import os, os.path as opth

class _HatHImg:
    def __init__(self, raw_str, gid, zfill_len = 3):
        self.id, _t, self.filename = raw_str.split()
        self.id = self.id.zfill(zfill_len)
        self.hash, self.length, self.width, self.height, self.format = _t.split('-')
        self.hash10 = self.hash[:10]
        self.gid = gid

    def url(self, isEX = False):
        return 'http://%s.org/s/%s/%d-%d' % \
            ((isEX and 'exhentai' or 'g.e-hentai'), self.hash10, self.gid, self.id)

class HatH:
    def __init__(self, dirpath = '', filename = '', stream = '', overwrite = False):
        if filename:
            with open(filename, 'r') as f:
                lines = f.readlines()
        elif stream:
            lines = stream.split('\n')
        else:
            raise TypeError("Either filename or stream must be specified.")
        self.overwrite = overwrite
        self._imglist = []
        self._parse_content(lines)
        self.setpath(dirpath)
    
    def _parse_content(self, lines):
        #Don't worry. For 2048 lines pop() uses 1ms, pop(0) uses 3ms
        self.gid = int(lines.pop(0)[4:])#GID xxx
        self.count = int(lines.pop(0)[6:])#FILES xxx
        self.name = lines.pop(0)[6:]#TITLE xxx
        lines.pop(0)
        lines.pop(0)
        _next = lines.pop(0)
        zero_len = int(math.log(self.count) / math.log(10)) + 1
        while _next != 'INFORMATION\n':
            if _next != '\n':
                self._imglist.append(_HatHImg(_next.strip(), self.gid, zero_len))
            _next = lines.pop(0)
        self.title = lines.pop(0)[14:]#'Title:        '
        self.upload_time = lines.pop(0)[14:]#'Upload Time:  '
        self.uploader_by = lines.pop(0)[14:]#Uploaded By:  '
        self.downloaded = lines.pop(0)[14:]#'Downloaded:   '
        self.tags = lines.pop(0)[14:].split(',')#'Downloaded:   '

    def setpath(self, path = None):
        if path:
            self.dirpath = path
        else:
            self.dirpath = self.name.decode('utf-8')
        if not self.overwrite:
            self.reload_list()

    def reload_list(self):
        i = 0
        while True:
            if opth.exists(opth.join(self.dirpath, '%s.%s' % 
                            (self._imglist[i].id, self._imglist[i].format))):
                del(self._imglist[i])
            i += 1
            if i >= len(self._imglist):
                break
        self.count = len(self._imglist)

    def renameToSeq(self, path = None):
        if not path:
            path = self.dirpath
        for i in range(self.count):
            oriname = self._imglist[i].name
            seqname = '%s.%s' % (int(self._imglist[i].id), self._imglist[i].format)
            if opth.exists(opth.join(path, oriname)):
                if opth.exists(opth.join(path, seqname)):
                    i = 1
                    while opth.exists(opth.join(path, seqname.replace('.', '-%d.' % i))):
                        i += 1
                    os.rename(opth.join(path, oriname), opth.join(path, seqname.replace('.', '-%d.' % i)))
                else:
                    os.rename(opth.join(path, oriname), opth.join(path, seqname))

    def renameToOri(self, path = None):
        if not path:
            path = self.dirpath
        for i in range(self.count):
            oriname = self._imglist[i].name
            seqname = '%s.%s' % (int(self._imglist[i].id), self._imglist[i].format)
            if opth.exists(opth.join(path, seqname)):
                if opth.exists(opth.join(path, oriname)):
                    i = 1
                    while opth.exists(opth.join(path, oriname.replace('.', '-%d.' % i))):
                        i += 1
                    os.rename(opth.join(path, seqname), opth.join(path, oriname.replace('.', '-%d.' % i)))
                else:
                    os.rename(opth.join(path, seqname), opth.join(path, oriname))

    def __len__(self):
        return self.count
    
    def htmlescape(self, str):
        def replc(match):
            # print match.group(0),match.group(1),match.group(2)
            dict = {'amp':'&', 'nbsp':' ', 'quot':'"', 'lt':'<', 'gt':'>', 'copy':'©', 'reg':'®'}
            # dict+={'∀':'forall','∂':'part','∃':'exist','∅':'empty','∇':'nabla','∈':'isin','∉':'notin','∋':'ni','∏':'prod','∑':'sum','−':'minus','∗':'lowast','√':'radic','∝':'prop','∞':'infin','∠':'ang','∧':'and','∨':'or','∩':'cap','∪':'cup','∫':'int','∴':'there4','∼':'sim','≅':'cong','≈':'asymp','≠':'ne','≡':'equiv','≤':'le','≥':'ge','⊂':'sub','⊃':'sup','⊄':'nsub','⊆':'sube','⊇':'supe','⊕':'oplus','⊗':'otimes','⊥':'perp','⋅':'sdot','Α':'Alpha','Β':'Beta','Γ':'Gamma','Δ':'Delta','Ε':'Epsilon','Ζ':'Zeta','Η':'Eta','Θ':'Theta','Ι':'Iota','Κ':'Kappa','Λ':'Lambda','Μ':'Mu','Ν':'Nu','Ξ':'Xi','Ο':'Omicron','Π':'Pi','Ρ':'Rho','Σ':'Sigma','Τ':'Tau','Υ':'Upsilon','Φ':'Phi','Χ':'Chi','Ψ':'Psi','Ω':'Omega','α':'alpha','β':'beta','γ':'gamma','δ':'delta','ε':'epsilon','ζ':'zeta','η':'eta','θ':'theta','ι':'iota','κ':'kappa','λ':'lambda','μ':'mu','ν':'nu','ξ':'xi','ο':'omicron','π':'pi','ρ':'rho','ς':'sigmaf','σ':'sigma','τ':'tau','υ':'upsilon','φ':'phi','χ':'chi','ψ':'psi','ω':'omega','ϑ':'thetasym','ϒ':'upsih','ϖ':'piv','Œ':'OElig','œ':'oelig','Š':'Scaron','š':'scaron','Ÿ':'Yuml','ƒ':'fnof','ˆ':'circ','˜':'tilde',' ':'ensp',' ':'emsp',' ':'thinsp','‌':'zwnj','‍':'zwj','‎':'lrm','‏':'rlm','–':'ndash','—':'mdash','‘':'lsquo','’':'rsquo','‚':'sbquo','“':'ldquo','”':'rdquo','„':'bdquo','†':'dagger','‡':'Dagger','•':'bull','…':'hellip','‰':'permil','′':'prime','″':'Prime','‹':'lsaquo','›':'rsaquo','‾':'oline','€':'euro','™':'trade','←':'larr','↑':'uarr','→':'rarr','↓':'darr','↔':'harr','↵':'crarr','⌈':'lceil','⌉':'rceil','⌊':'lfloor','⌋':'rfloor','◊':'loz','♠':'spades','♣':'clubs','♥':'hearts','♦':'diams'}
            if match.groups > 2:
                if match.group(1) == '#':
                    return unichr(int(match.group(2)))
                else:
                    return  dict.get(match.group(2), '?')
        htmlre = re.compile("&(#?)(\d{1,5}|\w{1,8}|[a-z]+);")
        return htmlre.sub(replc, str)


if __name__ == '__main__':
    a = HatH(filename = r'Z:\EHG-688702.hathdl')
    print a.count
    a.setpath(r'Z:\test')
    print a.count
