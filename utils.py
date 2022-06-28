#! /usr/bin/env python3
# -*- coding:utf8 -*-

_assoc = [1,35,38,40,15,25,33,32,18,23,28,31,20,21,22,30,55,45,43,41,5,2,36,39,13,16,26,34,12,19,24,29,58,53,48,42,63,56,46,44,8,6,3,37,11,14,17,27,60,52,51,50,61,59,54,49,62,64,57,47,10,9,7,4]

def coord_3d_to_linear(x, y, z):
    assert(x >= 0 and x <= 3 and y >=0 and y <=3 and z >= 0 and z <= 3)
    return _assoc[x*16+z*4+y]-1

def coord_linear_to_3d(n):
    assert(n >= 0 and n <= 63)
    pos = _assoc.index(n+1)
    return (pos//16, pos % 4, (pos % 16)//4)
