#!/usr/bin/env python2.7

from jug import TaskGenerator,barrier


@TaskGenerator
def minimain(n):
    print 'minimain %d finished' % n

@TaskGenerator
def main(n):
    
    nn = range(10)
    map(minimain,nn)
    barrier()
    print 'main finished??'

map(main,[1])
