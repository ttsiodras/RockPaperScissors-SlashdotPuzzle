#!/usr/bin/env python2

# You'd better run this with Pypy - tremendous speedup compared to CPython!

from collections import namedtuple

Stats = namedtuple('stats', ['r', 'p', 's'])


def evl(a, b):
    '''
    Returns the chances of winning of player a against player b,
    using the two players' probabilities - rock beats scissors,
    but loses from paper, so if a plays rock, the expected gain
    is a.r * (b.s - b.p) ... etc.
    '''
    return a.r * (b.s - b.p) + a.p * (b.r - b.s) + a.s * (b.p - b.r)

# Scanning for solution in probability steps of 0.01 (with Pypy, this
# finds the solution in 3 seconds on my Atom330).
best = 1., None
for me_rock in xrange(0, 101):
    for me_paper in xrange(0, 101 - me_rock):
        mr, mp = me_rock / 100., me_paper / 100.
        ms = (100 - me_rock - me_paper) / 100.
        assert(ms >= 0.)
        me = Stats(mr, mp, ms)
        best_for_him = -1., None
        for his_rock in xrange(50, 101):
            for his_paper in xrange(0, 101 - his_rock):
                hr, hp = his_rock / 100., his_paper / 100.
                hs = (100 - his_rock - his_paper) / 100.
                assert(hs >= 0.)
                him = Stats(hr, hp, hs)
                res = evl(him, me)
                if res > best_for_him[0]:
                    best_for_him = res, him
        if best[0] > best_for_him[0]:
            best = best_for_him[0], best_for_him[1], me

print best
# Results
# best[0] = -0.165
# best[1] = best_for_him = stats(r=0.5, p=0.0, s=0.5)
# best[2] = best_for_me  = stats(r=0.33, p=0.67, s=0.0)

# Simulation of the solution, just for kicks

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

print "Wins:", wins, "Draws:", draws, "Losses:", losses
