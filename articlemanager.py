# -*- coding: utf-8 -*-

import const
import os
import threading, time,codecs

BLOGPATH = const.BLOGPATH
POSTSPATH = os.path.join(BLOGPATH, 'source', '_posts')

def create_worker(title,titleascii,article, photos):
    filename = os.path.join(POSTSPATH,time.strftime("%Y-%m-%d", time.localtime())+'-%s.md'%titleascii.replace(' ','-'))
    try:
        os.system('cd %s && git pull'%BLOGPATH)
        with codecs.open(filename, 'w', 'utf-8') as f:
            head = '''---
title: {}
date: {}
tags: 灌水
---
'''.format(title,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            f.write(head+article)
        for x in photos:
            os.system('mv %s %s/source/img/'%(x, BLOGPATH))
        os.system('cd %s && git add .'%BLOGPATH)
        os.system('cd %s && git commit -m telegram-bot-auto'%BLOGPATH)
        os.system('cd %s && git push'%BLOGPATH)
        os.system('cd %s && hexo g && hexo d'%BLOGPATH)
    except Exception as e:
        print(e)

def create(title,titleascii,article):
    # 异步create
    t = threading.Thread(target=create_worker,args=(title,titleascii,article))
    t.start()
    return t

def test():
    pass
        

if __name__ == '__main__':
    test()