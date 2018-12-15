#!/bin/python3
# -*- coding: utf-8 -*-

"""
NOT COMPLETE

Time: 2h (WITH KIDS!)
"""


import math
import os
import random
import re
import sys

DEBUG = False
DEBUG_FUNCTIONS = False

#
# Complete the 'minOperations' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts LONG_INTEGER n as parameter.
#

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


class Memoize:
	def __init__(self, fn):
		self.fn = fn
		self.memo = {}

	def __call__(self, *args):
		if args not in self.memo:
			self.memo[args] = self.fn(*args)
		return self.memo[args]

@Memoize
@debugDecorator()
def transform_until_changeable(b, curr_c):
	if b == "":
		return curr_c, ""
	
	if b == "0":
		# Change to 1!
		c = curr_c + 1
		b1 = "1"
		if DEBUG: print("%4s: %6s (+1)" % (c, b1))
		return c, b1
	
	if b == "1":
		return curr_c, "1"
	
	if b[0] == "0":
		c, b1 = transform_until_changeable(b[1:], curr_c)
		
		# Change to 1!
		c += 1
		b1 = "1"+b1
		if DEBUG: print("%4s: %6s (+1)" % (c, b1))
		
		# Change the following to 0!
		c,b2 = transform_to_zero(b1[1:], c)
		b1 = "1"+b2
		if DEBUG: print("%4s: %6s" % (c, b1))
		
		return c, b1
	
	if b[0] == "1":
		c, b1 = transform_to_zero(b[1:], curr_c)
		b1 = "1"+b1
		return c, b1

@Memoize
@debugDecorator()
def transform_to_zero(b, curr_c):
	if b == "":
		return curr_c, ""
	
	if b == "0":
		return curr_c, "0"
	
	if b == "1":
		# Change to 0!
		c = curr_c + 1
		b1 = "0"
		if DEBUG: print("%4s: %6s (+1)" % (c, b1))
		return c, b1
	
	if b[0] == "0":
		c, b1 = transform_to_zero(b[1:], curr_c)
		b1 = "0"+b1
		if DEBUG: print("%4s: %6s" % (c, b1))
		return c, b1
	
	else:
		c, b1 = transform_until_changeable(b[1:], curr_c)
		
		# Change to 0!
		c += 1
		b1 = "0"+b1
		if DEBUG: print("%4s: %6s (+1)" % (c,b1))
		
		# Change the following to 0!
		c, b2 = transform_to_zero(b1[1:], c)
		b1 = "0" + b2
		if DEBUG: print("%4s: %6s" % (c, b1))
		
		return c, b1

def minOperations(n):
	b = bin(n)[2:]
	if DEBUG: print("> %s"%b)
	
	c, b1 = transform_to_zero(b, 0)
	
	return c
	

if __name__ == '__main__':
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout

	n = int(input().strip())

	result = minOperations(n)

	fptr.write(str(result) + '\n')

	fptr.close()
