#!/usr/bin/env python2

from collections import namedtuple
Stats = namedtuple('stats', ['r', 'p', 's'])

def evl(a, b):
    return a.r * (b.s - b.p) + a.p * (b.r - b.s) + a.s * (b.p - b.r)

# Scanning for solution in probability steps of 0.01
best = 1., None
for me_rock in xrange(0, 101):
    for me_paper in xrange(0, 101 - me_rock):
        mr, mp = me_rock / 100., me_paper / 100.
        ms = 1. - mr - mp
        if ms < 0.:
            continue
        me = Stats(mr, mp, ms)
        best_for_him = -1., None
        for his_rock in xrange(50, 101):
            for his_paper in xrange(0, 101 - his_rock):
                hr, hp = his_rock / 100., his_paper / 100.
                hs = 1. - hr - hp
                if hs < 0.:
                    continue
                him = Stats(hr, hp, hs)
                res = evl(him, me)
                if res > best_for_him[0]:
                    best_for_him = res, him
        if best[0] > best_for_him[0]:
            best = best_for_him[0], best_for_him[1], me

print best
# Results
# best[0] = -0.16000000000000006
# best[1] = best_for_him = stats(r=0.5, p=0.0, s=0.5)
# best[2] = best_for_me  = stats(r=0.33, p=0.66, s=0.009999999999999898)

# simulation

import random

him, me = best[1], best[2]
wins, draws, losses = 0, 0, 0
for i in xrange(10000):
    if random.random() < me.r:  iplay = 'r'
    else:                       iplay = 'p'
    if random.random() < him.r: heplays = 'r'
    else:                       heplays = 's'

    if iplay == heplays:                   draws += 1
    elif iplay == 'r' and heplays == 's':  wins += 1
    elif iplay == 'p' and heplays == 'r':  wins += 1
    elif iplay == 'p' and heplays == 's':  losses += 1

print wins, draws, losses
