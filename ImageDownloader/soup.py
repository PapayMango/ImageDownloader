import requests as req
from bs4 import BeautifulSoup as bs
import re
from . import acl
from . import regex as rg
from . import views as vi
import sys
from pathlib import Path 

IMAGE_ROOT_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = IMAGE_ROOT_DIR/'images/'
STR_IMAGE_DIR = str(IMAGE_DIR) + '/'
print(STR_IMAGE_DIR)
MAX_DEPTH = 2

sys.setrecursionlimit(2000)
print(sys.getrecursionlimit())
count = 0

def dl(url,depth=0,ulist=None,hlist=None):
# def dl(url,depth=0,ulist=None,hlist=tree()):
    print('dl start')
    depth_ = depth
    url_ = url
    # max_depth = 1

    if ulist is None:
        list_ = tree()
    else:
        list_ = ulist
    if hlist is None:
        hlist_ = tree()
    else:
        hlist_ = hlist

    # hlist_ = hlist
    # list_ = ulist
    processes = 0
    progress = 0

    global count

    def imageDL(src,flag):
        try:
            if flag and not hlist_.append(src):
                return False
            r = rg.P_imageDL.search(src).group()

            name = STR_IMAGE_DIR + r
            r = req.get(src)
            image = r.content
            size = r.headers.get('content-length',-1)
            if int(size) > 100000:
                with open(name,'wb') as h:
                    h.write(image)
        except Exception as e:
            print(e)
        return True

    def atag(tag):
        if tag.name=='a' and tag.has_attr('href'):
            url = tag['href']
            if rg.P_reshapeURL_a.match(url):
                r = rg.P_reshapeURL_g.findall(url)
                if not r[0] in acl.wl:
                    return False
                else:
                    url = rg.P_reshapeSrc_b.match(url_).group() + url
            elif rg.P_reshapeURL_e.match(url):
                return False
            elif rg.P_reshapeURL_c.match(url):
                url = rg.P_reshapeURL_d.match(url_).group() + url
            elif rg.P_reshapeURL_f.search(url): 
                r = rg.P_reshapeURL_g.findall(url)
                if not r[1] in acl.wl:
                    return False
            r = rg.P_reshapeURL_i.search(url) 
            if r:
                url = url[0:r.start()]
            r = re.search('\?[^/]+$',url)
            if r:
                url = url[0:r.start()]
            r = rg.P_reshapeURL_h.search(url)
            if r and r.group() in ['.png','.jpg','.tif','.gif','.jpeg']:
                imageDL(url,True)
                return False
            tag['href'] = url
            # if depth_ == max_depth:
            if depth_ == MAX_DEPTH:
                return False
            return list_.append(url)
        return False

    def imgtag(tag):
        if tag.name=='img':
            if tag.has_attr('src'):
                src = tag['src']
                if rg.P_reshapeURL_a.match(src):
                    r = rg.P_reshapeURL_g.findall(src)
                    if not r[0] in acl.wl:
                        return False
                    else:
                        src = rg.P_reshapeSrc_b.match(url_).group() + src
                elif rg.P_reshapeURL_f.match(src):
                    r = rg.P_reshapeURL_g.findall(src)
                    if not r[1] in acl.wl:
                        return False
                elif rg.P_reshapeSrc_c.match(src):
                    src = rg.P_reshapeSrc_d.match(url_).group() + src
                tag['src'] = src
                return hlist_.append(src)
            return True
        return False

    def reshapeURL(url):
        url__ = url
        return url__,True

    def reshapeSrc(src):
        src_ = src
        if rg.P_reshapeSrc_a.match(src_) :
            src_ = rg.P_reshapeSrc_b.match(url_).group() + src_
        if rg.P_reshapeSrc_c.match(src_):
            src_ = rg.P_reshapeSrc_d.match(url_).group() + src_
        return src_

    r = req.get(url_)
    s = bs(r.text,'lxml')
    a = s.find_all(atag)
    i = s.find_all(imgtag)

    if depth_ == 0:
        processes = len(a)
        vi.set_total(processes)

    for b in i:
        try:
            if b.has_attr('data-src'):
                src_ = reshapeSrc(b['data-src'])
            else:    
                src_ = b['src']
            imageDL(src_,False)
        except Exception as e:
            print(e)
    for c in a:
        try:
            dl(c['href'],depth_+1,list_,hlist_)
            if depth_ == 0:
                progress += 1
                vi.set_process(progress)
                print(' progress ' + str(progress) + ' in ' + str(processes))
        except Exception as e:
            print(e)
    return True

# class tree:
#     def __init__(self):
#         self.tree = []
#     def append(self,a):
#         c = 1
#         index = 0
#         r = rg.P_reshapeURL_g.findall(a)
#         r = r[1:len(r)]
#         for a in r:
#             if len(self.tree) == index:
#                 self.tree.append({}) 
#             l = self.tree[index]
#             if a in l:
#                 if len(r) == c:
#                     return False
#                 if l[a] == 0:
#                     l[a] = len(self.tree)
#                 index = l[a]
#             else:
#                 if len(r) == c:
#                     l[a] = 0
#                     return True
#                 l[a] = len(self.tree)
#                 index = l[a]
#             c = c + 1
#         return True
class tree:
    def __init__(self):
        self.tree = []
    def append(self,a):
        # print('tree : ' + str(self.tree))
        c = 1
        index = 0
        r = rg.P_reshapeURL_g.findall(a)
        r = r[1:len(r)]
        for a in r:
            if len(self.tree) == index:
                self.tree.append({})
                self.tree[index]['set'] = set()
            l = self.tree[index]
            # if a in l:
            if a in l['set']:
                if len(r) == c:
                    return False
                if l[a] == 0:
                    l[a] = len(self.tree)
                index = l[a]
            else:
                l['set'].add(a)
                if len(r) == c:
                    l[a] = 0
                    return True
                l[a] = len(self.tree)
                index = l[a]
            c = c + 1
        # print('tree : ' + str(self.tree))
        return True