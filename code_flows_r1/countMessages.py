#!/bin/python3
#  -*- coding: utf-8 -*-

"""
Time: 3h10m
"""

import math
import os
import random
import re
import sys

import pprint

# import operator as op
# from functools import reduce

#
# Complete the 'countMessages' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. STRING_ARRAY keys
#  2. STRING message
#

DEBUG = False

# ---------------------------------------- #

# def nCr(n, r):
# 	r = min(r, n-r)
# 	numer = reduce(op.mul, range(n, n-r, -1), 1)
# 	denom = reduce(op.mul, range(1, r+1), 1)
# 	return numer / denom

# ---------------------------------------- #

MAGIC_NUM = 1000000007

def mul(a, b):
	return (a*b) % MAGIC_NUM

# ---------------------------------------- #

precalc_x = {
	(1, 3): 1,
	(2, 3): 2,
	(3, 3): 4,
	
	(1, 4): 1,
	(2, 4): 2,
	(3, 4): 4,
	(4, 4): 8,
}

precalc_max_n = {
	3: 3,
	4: 4,
}

def X(n, c):
	# Space
	if c == 1:
		if DEBUG: print("X(%s,%s) = %s (-)" % (n,c,1))
		return 1
	
	# Out of range
	if n <= 0:
		if DEBUG: print("X(%s,%s) = %s (-)" % (n,c,0))
		return 0
	
	# Already in cache
	if (n, c) in precalc_x:
		x = precalc_x[(n, c)]
		if DEBUG: print("X(%s,%s) = %s (cached)" % (n,c,x))
		return x
	
	# Feed the cache (in order to avoid recursion error)
	if n > precalc_max_n[c]:
		if DEBUG: print("> > > > > > >")
		for i in range(precalc_max_n[c]+1, n+1):
			precalc_max_n[c] += 1
			X(i, c)
		if DEBUG: print("< < < < < < <")
	
	# Real calculation
	x = 1
	for j in range(1, c + 1):
		x += mul(
			x, 
			X(n-j, c)
		)
	
	precalc_x[(n,c)] = x
	if DEBUG: print("X(%s,%s) = %s" % (n, c, x))
	return x

# ---------------------------------------- #

def get_keys(keys, char):
	if DEBUG: print("%r -> %r" % (char, keys))
	for i,seq in enumerate(keys):
		if char in seq:
			key = i+1
			return str(key) * (seq.find(char)+1)
	raise Exception("xx")

# ---------------------------------------- #

def countMessages(keys, message):
	# Add " " to seq
	keys.insert(0, " ")
	
	# Normalize
	message = message.upper()
	_keys = []
	for k in keys:
		_keys.append(k.upper())
	keys = keys
	
	# Calc the num keys pressed 
	keys_seq = ""
	
	for char in message:
		keys_pressed = get_keys(keys, char)
		keys_seq += keys_pressed
	
	if DEBUG: print(keys_seq)
	
	# Calc all possible combinations
	comb = 1
	
	i = 1
	last_key = keys_seq[0]
	last_stroke_len = 1
	
	while i < len(keys_seq):
		if keys_seq[i] != last_key:
			# stroke finished
			c = len(keys[int(last_key)-1])
			comb = mul(
				comb,
				X(last_stroke_len, c)
			)
			# let's move on
			last_key = keys_seq[i]
			last_stroke_len = 1
		else:
			last_stroke_len += 1
		i += 1
		
	# stroke finished (out-of-cycle iteration)
	c = len(keys[int(last_key) - 1])
	comb = mul(
		comb,
		X(last_stroke_len, c)
	)
	
	if DEBUG: pprint.pprint(precalc_x)
	return comb

# ---------------------------------------- #

if __name__ == '__main__':
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout

	keys_count = int(input().strip())

	keys = []

	for _ in range(keys_count):
		keys_item = input()
		keys.append(keys_item)

	message = input()

	result = countMessages(keys, message)

	fptr.write(str(result) + '\n')

	fptr.close()
