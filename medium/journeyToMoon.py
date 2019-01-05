#!/bin/python3
# -*- coding: utf-8 -*-

"""
Result: 15/15
Time: 20m+40m
"""

import math
import os
import random
import re
import sys

DEBUG = True

# ---------------------------------------- #

# Complete the journeyToMoon function below.
def journeyToMoon(n, astronaut):
	
	# Group astronauts by country
	total = set()
	countries = []
	for a in astronaut:
		total.update(a)
		
		a1, a2 = a
		added = None
		for c in list(countries):
			if (a1 in c) or (a2 in c):
				if added:
					countries.remove(c)
					added.update(c)
				else:
					c.update(a)
					added = c
		
		if not added:
			countries.append(set(a))
		
		if DEBUG: print(a)
		if DEBUG: print(countries)
		
	# For every possible astronaut from 0 to n, if it is not contained in current groups it makes a group by his own
	for i in range(0,n):
		if i not in total:
			countries.append({i})
		
	if DEBUG: print(countries)
	
	combs = 0
	for c in countries:
		combs += len(c) * (n - len(c))
	
	# Divide by the number of possible permutations of two elements
	return round(combs / 2)

# ---------------------------------------- #

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	np = input().split()
	
	n = int(np[0])
	
	p = int(np[1])
	
	astronaut = []
	
	for _ in range(p):
		astronaut.append(list(map(int, input().rstrip().split())))
	
	result = journeyToMoon(n, astronaut)
	
	fptr.write(str(result) + '\n')
	
	fptr.close()

if __name__ == '__main__':
	main()
