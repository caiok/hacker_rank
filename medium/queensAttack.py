#!/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.hackerrank.com/challenges/queens-attack-2/problem

Time 22m
"""

import math
import os
import random
import re
import sys

DIRECTIONS = {
	"N":  (+1, 0),
	"NE": (+1,+1),
	"E":  ( 0,+1),
	"SE": (-1,+1),
	"S":  (-1, 0),
	"SW": (-1,-1),
	"W":  ( 0,-1),
	"NW": (+1,-1)
}

# Complete the queensAttack function below.
def queensAttack(n, k, r_q, c_q, obstacles):
	obs = set()
	for o in obstacles:
		obs.add((o[0],o[1]))
	
	count = 0
	
	for dir,offsets in DIRECTIONS.items():
		r_curr = r_q + offsets[0]
		c_curr = c_q + offsets[1]
		
		while ((r_curr,c_curr) not in obs) and (1 <= r_curr <= n) and (1 <= c_curr <= n):
			#print("%(dir)s -> %(r_curr)s,%(c_curr)s" % vars())
			count += 1
			r_curr += offsets[0]
			c_curr += offsets[1]
	
	return count

# ===================================================================== #

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	nk = input().split()
	
	n = int(nk[0])
	
	k = int(nk[1])
	
	r_qC_q = input().split()
	
	r_q = int(r_qC_q[0])
	
	c_q = int(r_qC_q[1])
	
	obstacles = []
	
	for _ in range(k):
		obstacles.append(list(map(int, input().rstrip().split())))
	
	result = queensAttack(n, k, r_q, c_q, obstacles)
	
	fptr.write(str(result) + '\n')
	
	fptr.close()

if __name__ == '__main__':
	main()
