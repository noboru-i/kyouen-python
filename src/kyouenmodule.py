#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
'''
Created on 2012/06/21

@author: noboru
'''

import logging
import math
from numpy import *

def getPoints(stoneStr, size=0):
    if (size == 0):
        size = math.sqrt(stoneStr.length)
    stones = []
    for i, s in enumerate(stoneStr):
        if s == "1":
            x = i % size
            y = i / size
            stones.append(array([float(x), float(y)]))
    return stones
    
import itertools
def hasKyouen(stonePoints):
    if (len(stonePoints) < 4):
        return False
    
    for stones in itertools.combinations(stonePoints, 4):
        if(isKyouen(stones) != None):
            return True
    return False

def isKyouen(stones):
    # p1,p2の垂直二等分線を求める
    l12 = getMidperpendicular(stones[0], stones[1]);
    # p2,p3の垂直二等分線を求める
    l23 = getMidperpendicular(stones[2], stones[3]);

    # 交点を求める
    intersection123 = getIntersection(l12, l23);
    if (intersection123 == None):
        # p1,p2,p3が直線上に存在する場合
        logging.debug('line')
        l34 = getMidperpendicular(stones[2], stones[3]);
        intersection234 = getIntersection(l23, l34);
        if (intersection234 == None):
            # p2,p3,p4が直線状に存在する場合
            return (stones);
    else:
        dist1 = getDistance(stones[0], intersection123);
        dist2 = getDistance(stones[3], intersection123);
        if (math.fabs(dist1 - dist2) < 0.0000001):
            logging.debug('circle')
            return (stones, intersection123, dist1);
    return None

def getDistance(p1, p2):
    dist = p1 - p2
    return math.hypot(dist[0], dist[1])
    
def getIntersection(l1, l2):
    f1 = l1[1][0] - l1[0][0]
    g1 = l1[1][1] - l1[0][1]
    f2 = l2[1][0] - l2[0][0]
    g2 = l2[1][1] - l2[0][1]
    
    det = f2 * g1 - f1 * g2
    if (det == 0):
        return None
    
    dx = l2[0][0] - l1[0][0]
    dy = l2[0][1] - l1[0][1]
    t1 = (f2 * dy - g2 * dx) / det
    
    return [l1[0][0] + f1 * t1, l1[0][1] + g1 * t1]
    
    
def getMidperpendicular(p1, p2):
    midpoint = getMidpoint(p1, p2);
    dif = p1 - p2;
    gradient = [dif[1], dif[0] * -1]

    return [midpoint, midpoint + gradient];

def getMidpoint(p1, p2):
    return (p1 + p2) / 2

if __name__ == '__main__':
    stones = getPoints("000000000000000000000000000000000000")
    print hasKyouen(stones)