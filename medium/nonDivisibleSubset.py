#!/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.hackerrank.com/challenges/non-divisible-subset

Time: 1h35m NOT RESOLVED

"""

import math
import os
import random
import re
import sys

import collections
from collections import OrderedDict

class OrderedSet(collections.MutableSet):

	def __init__(self, iterable=None):
		self.end = end = [] 
		end += [None, end, end]		 # sentinel node for doubly linked list
		self.map = {}				   # key --> [key, prev, next]
		if iterable is not None:
			self |= iterable

	def __len__(self):
		return len(self.map)

	def __contains__(self, key):
		return key in self.map

	def add(self, key):
		if key not in self.map:
			end = self.end
			curr = end[1]
			curr[2] = end[1] = self.map[key] = [key, curr, end]

	def discard(self, key):
		if key in self.map:		
			key, prev, next = self.map.pop(key)
			prev[2] = next
			next[1] = prev

	def __iter__(self):
		end = self.end
		curr = end[2]
		while curr is not end:
			yield curr[0]
			curr = curr[2]

	def __reversed__(self):
		end = self.end
		curr = end[1]
		while curr is not end:
			yield curr[0]
			curr = curr[1]

	def pop(self, last=True):
		if not self:
			raise KeyError('set is empty')
		key = self.end[1][0] if last else self.end[2][0]
		self.discard(key)
		return key

	def __repr__(self):
		if not self:
			return '%s()' % (self.__class__.__name__,)
		return '%s(%r)' % (self.__class__.__name__, list(self))

	def __eq__(self, other):
		if isinstance(other, OrderedSet):
			return len(self) == len(other) and list(self) == list(other)
		return set(self) == set(other)

# ======================================================================= #


# Complete the nonDivisibleSubset function below.
def nonDivisibleSubset(k, S):
	# All the intersections
	m = {}
	
	for s1 in S:
		m[s1] = set()
		for s2 in S:
			if s1 != s2:
				if (s1 + s2) % k != 0:
					m[s1].add(s2)

	# All numbers ordered by who has the highest siblings number
	r = []
	
	for k,v in m.items():
		r.append((k,len(v)))
	
	r.sort(key=lambda x: x[1], reverse=True)
	
	# Map with all numbers and their positions in r
	r_pos = {}
	for i,e in enumerate(r):
		r_pos[e[0]] = i
	
	# Ordered initial list with ordered sets
	m2 = OrderedDict()
	
	for n,h in r:
		m2[n] = OrderedSet(sorted(m[n], key=lambda x: r_pos[x]))

	print("m=%s"%m)
	print("r=%s"%r)
	print("r_pos=%s"%r_pos)
	print("m2=%s"%m2)
	
	# Calculations
	# ...

# ----------------------------------------------------------------------- #

def nonDivisibleSubset_solution(k, S):
	counts = [0] * k
	for number in numbers:
		counts[number % k] += 1
	
	count = min(counts[0], 1)
	for i in range(1, k // 2 + 1):
		if i != k - i:
			count += max(counts[i], counts[k - i])
	if k % 2 == 0:
		count += 1
	
	print
	count

# ======================================================================= #

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	nk = input().split()

	n = int(nk[0])
	k = int(nk[1])

	S = list(map(int, input().rstrip().split()))

	result = nonDivisibleSubset(k, S)
	
	fptr.write(str(result) + '\n')
	fptr.close()

if __name__ == '__main__':
	#main()
	
	nonDivisibleSubset(4, [1,2,3,4,5,6])
