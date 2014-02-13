#!/usr/bin python
# -*- coding:utf-8 -*-

import hashlib
import time
from multiprocessing import Process
from itertools import islice
import math

_pass = '567890'
_salt = 'hoge'
_hash = hashlib.md5(_salt + '$' + _pass).hexdigest()


# Yakst - Pythonスクリプトのパフォーマンス計測ガイド
# http://yakst.com/ja/posts/42
class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs


def get_hash(salt, password):
    pwd = "%06d" % password
    return hashlib.md5(salt + '$' + pwd).hexdigest()


def pwd_check(arg):
    return get_hash(_salt, arg) == _hash


def task(num, numbers):
    # q.put([i for i in numbers if pwd_check(i)])
    with Timer() as t:
        for i in numbers:
            if pwd_check(i):
                print "password: %s" % i
                break
    print "=> process%d elasped times: %s s" % (num, t.secs)


def multi():
    limit = 1000000
    workers = 4
    tasks = int(math.ceil(float(limit)/float(workers)))

    limit_loop = xrange(limit)
    jobs = [Process(
        target=task,
        args=(i, islice(limit_loop, tasks*i, tasks*(i+1))))
        for i in xrange(workers)]

    for job in jobs:
        job.start()


def non_multi():
    limit = 1000000
    for i in xrange(limit):
        if pwd_check(i):
            print "password: %s" % i
            return


if __name__ == '__main__':
    print "pass: %s\nsalt: %s\nhash: %s" % (_pass, _salt, _hash)

    print "\nNon MultiProcessing..."
    with Timer() as t:
        non_multi()
    print "=> elasped times: %s s" % t.secs

    print "\nMultiProcessing..."
    multi()
