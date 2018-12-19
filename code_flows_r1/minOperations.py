#!/bin/python3
# -*- coding: utf-8 -*-

"""
Points: 75
Result: 8/8

Time: 2h
"""


import math
import os
import random
import re
import sys

DEBUG = False
DEBUG_FUNCTIONS = False
MEMOIZE = True

# =========================================================================== #

class Logger(object):
	indent = 0
	active = DEBUG_FUNCTIONS
	
	def indent_inc(self):
		self.indent += 1
	
	def indent_dec(self):
		self.indent -= 1
		
	def log(self, m):
		if self.active:
			print(" "*self.indent + m)

logger = Logger()

# --------------------------------------------------------------------------- #

def debugDecorator():
	def _decorator(fn):
		def _decorated(*arg, **kwargs):
			logger.indent_inc()
			logger.log("calling '%s'(%r,%r)" % (fn.__name__, arg, kwargs))
			
			ret = fn(*arg, **kwargs)
			
			logger.log("called  '%s'(%r,%r) got return value: %r" % (fn.__name__, arg, kwargs, ret))
			logger.indent_dec()
			
			return ret
		
		return _decorated
	
	return _decorator

# --------------------------------------------------------------------------- #

stats = {}

class Memoize:
	
	def __init__(self, fn):
		self.fn = fn
		self.memo = {}
		self.__name__ = fn.__name__
		stats[fn.__name__] = {'hits':0, 'misses':0}

	def __call__(self, *args):
		if not MEMOIZE or args not in self.memo:
			if DEBUG_FUNCTIONS: print("Cache MISS %s(%s)" % (self.fn.__name__, args))
			stats[self.fn.__name__]['misses'] += 1
			res = self.fn(*args)
			self.memo[args] = res
			return res
		else:
			if DEBUG_FUNCTIONS: print("Cache HIT %s(%s)" % (self.fn.__name__, args))
			stats[self.fn.__name__]['hits'] += 1
			return self.memo[args]

# --------------------------------------------------------------------------- #

@debugDecorator()
@Memoize
def transform_until_changeable(b):
	if b == "":
		return 0, ""
	
	if b == "0":
		# Change to 1!
		c = 1
		b1 = "1"
		if DEBUG: print("%4s: %6s (+1)" % (c, b1))
		return c, b1
	
	if b == "1":
		return 0, "1"
	
	if b[0] == "0":
		c, b1 = transform_until_changeable(b[1:])
		
		# Change to 1!
		c += 1
		b1 = "1"+b1
		if DEBUG: print("%4s: %6s (+1)" % (c, b1))
		
		# Change the following to 0!
		c2, b2 = transform_to_zero(b1[1:])
		c += c2
		b1 = "1"+b2
		if DEBUG: print("%4s: %6s" % (c, b1))
		
		return c, b1
	
	if b[0] == "1":
		c, b1 = transform_to_zero(b[1:])
		b1 = "1"+b1
		return c, b1

# --------------------------------------------------------------------------- #

@debugDecorator()
@Memoize
def transform_to_zero(b):
	if b == "":
		return 0, ""
	
	if b == "0":
		return 0, "0"
	
	if b == "1":
		# Change to 0!
		c = 1
		b1 = "0"
		if DEBUG: print("%4s: %6s (+1)" % (c, b1))
		return c, b1
	
	if b[0] == "0":
		c, b1 = transform_to_zero(b[1:])
		b1 = "0"+b1
		if DEBUG: print("%4s: %6s" % (c, b1))
		return c, b1
	
	else:
		c, b1 = transform_until_changeable(b[1:])
		
		# Change to 0!
		c += 1
		b1 = "0"+b1
		if DEBUG: print("%4s: %6s (+1)" % (c,b1))
		
		# Change the following to 0!
		c2, b2 = transform_to_zero(b1[1:])
		c += c2
		b1 = "0" + b2
		if DEBUG: print("%4s: %6s" % (c, b1))
		
		return c, b1

# --------------------------------------------------------------------------- #

#
# Complete the 'minOperations' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts LONG_INTEGER n as parameter.
#

def minOperations(n):
	b = bin(n)[2:]
	if DEBUG: print("> %s"%b)
	
	c, b1 = transform_to_zero(b)
	
	return c

# =========================================================================== #

def test():
	global DEBUG, DEBUG_FUNCTIONS, MEMOIZE, logger
	DEBUG = True
	DEBUG_FUNCTIONS = True
	MEMOIZE = True
	logger.active = False
	
	print(">>>> %s <<<<" % minOperations(155599))
	
	#print(">>>> %s <<<<" % minOperations(100))
	
	print(stats)

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	n = int(input().strip())
	
	result = minOperations(n)
	
	fptr.write(str(result) + '\n')
	
	fptr.close()

if __name__ == '__main__':
	#test()
	main()
