#!/usr/bin python
# -*- coding:utf-8 -*-

import hashlib
import time
from multiprocessing import Process
from itertools import islice
import math
import sys

_pass = '567890'
_salt = 'hoge'
_hash = hashlib.md5(_salt + '$' + _pass).hexdigest()


def get_hash(salt, password):
    pwd = "%06d" % password
    return hashlib.md5(salt + '$' + pwd).hexdigest()


def pwd_check(arg):
    return get_hash(_salt, arg) == _hash


def task(num, numbers):
    start = time.time()
    for i in numbers:
        if pwd_check(i):
            print "password: %s" % i
            print "=> elapsed times: %s s" % (time.time() - start)
    print "=> process%d elasped times: %s s" % (num, time.time() - start)


def multi(processes):
    limit = 1000000
    workers = processes
    tasks = int(math.ceil(float(limit)/float(workers)))

    limit_loop = xrange(limit)
    jobs = [Process(
        target=task,
        args=(i, islice(limit_loop, tasks*i, tasks*(i+1))))
        for i in xrange(workers)]

    for job in jobs:
        job.start()

    if len(jobs) == 1:
        jobs[0].join()


def non_multi():
    limit = 1000000
    for i in xrange(limit):
        if pwd_check(i):
            print "password: %s" % i
            return


if __name__ == '__main__':
    try:
        processes = int(sys.argv[1])
    except:
        processes = 2

    print "pass: %s\nsalt: %s\nhash: %s" % (_pass, _salt, _hash)

    print "\nNon MultiProcessing..."
    multi(1)

    print "\nMultiProcessing..."
    multi(processes)
