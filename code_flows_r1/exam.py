#!/bin/python3
#  -*- coding: utf-8 -*-

"""
Time: 20m
"""

import math
import os
import random
import re
import sys



#
# Complete the 'exam' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY v as parameter.
#

def value(e):
	if e == 1:
		return 1
	else:
		return -1

def exam(v):
	me = 0
	my_friend = 0
	
	for e in v:
		my_friend += value(e)
	
	k = 0
	while k < len(v)-1:
		if (me > my_friend):
			return k
		
		me += value(v[k])
		my_friend -= value(v[k])
		k += 1
		
	return k

if __name__ == '__main__':
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	v_count = int(input().strip())
	
	v = []
	
	for _ in range(v_count):
		v_item = int(input().strip())
		v.append(v_item)
	
	result = exam(v)
	
	fptr.write(str(result) + '\n')
	
	fptr.close()
