#!/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.hackerrank.com/challenges/torque-and-development/problem

Time: 25m
"""

import math
import os
import random
import re
import sys

# Complete the roadsAndLibraries function below.
def roadsAndLibraries(n, c_lib, c_road, cities):
	if c_lib <= c_road:
		return n * c_lib
	
	graph = {}
	for c in range(1, n+1):
		graph[c] = set()
	
	for c1,c2 in cities:
		graph[c1].add(c2)
		graph[c2].add(c1)
	
	visited = set()
	to_visit = set()
	
	libraries = 0
	roads = 0
	
	for c in range(1, n+1):
		if c in visited:
			continue
		
		libraries += 1
		visited.add(c)
		to_visit.update(graph[c])
		
		while to_visit:
			c2 = to_visit.pop()
			if c2 not in visited:
				roads += 1
				visited.add(c2)
				to_visit.update(graph[c2])
	
	return libraries*c_lib + roads*c_road
		

if __name__ == '__main__':
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout

	q = int(input())

	for q_itr in range(q):
		nmC_libC_road = input().split()

		n = int(nmC_libC_road[0])

		m = int(nmC_libC_road[1])

		c_lib = int(nmC_libC_road[2])

		c_road = int(nmC_libC_road[3])

		cities = []

		for _ in range(m):
			cities.append(list(map(int, input().rstrip().split())))

		result = roadsAndLibraries(n, c_lib, c_road, cities)

		fptr.write(str(result) + '\n')

	fptr.close()
