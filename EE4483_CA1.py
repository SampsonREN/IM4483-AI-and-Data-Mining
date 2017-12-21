# -*- coding: utf-8 -*-
"""
EE4483
Implement TWO different search algorithms to find x^1/3 of any real number. 
Note negative number too. (10 points)
a. Please briefly explain the search strategies of the two algorithms.
b. Prove that your algorithms guarantee to find the correct answer.
c. Compare the two search algorithms and their complexity; explain which one is better
and why it is better. 
"""
import time


def binSearch (x,error):
    if x == 0:
        return 0
    if abs(x) >1:
        left  = min(x,x/abs(x))
        right = max(x,x/abs(x))
    else:
        left  = min(0,x/abs(x))
        right = max(0,x/abs(x))
    rt = (left+right)/2
    while abs(rt*rt*rt-x)>error:
            if rt*rt*rt > x:
                right = rt
            else:
                left = rt
            rt = (left+right)/2
    return rt

def newton(x, error):
    rt = x
    while abs(rt*rt*rt-x)>error:
        ## Assume y=rt^3-x, therefore we can use newton's method to find the root
        y=rt**3 - x
        rt = rt - y/(3*rt*rt)
    return rt

# Input #
x = -1
error = 0.0000001


start_time_B = time.clock()
rt1 = binSearch(x,error)
stop_time_B = time.clock()

start_time_N = time.clock()
rt2 = newton(x,error)
stop_time_N = time.clock()

print("--- %s seconds ---" % (stop_time_B - start_time_B))
print("The solution of " +str(x)+" from Binary Search is "+str(rt1))
print("--- %s seconds ---" % (stop_time_N - start_time_N))
print("The solution of " +str(x)+" from Newton Method is "+str(rt2))