#!/bin/python3
# -*- coding: utf-8 -*-

"""
Result: 3/8

Time: 13m+30m

Note: I can't manage to understand how to make the last 5 tests pass. Maybe I don't well understand the specs, I tried:
- Go ahead until it find an outfit it can't buy, then exit
- [My final choice] Go ahead until money is over or the list is over, skipping outfits too expensive for the current budget
- Sort all outfits by price ascending, than go ahead buying until money is over (a true getMaximumOutfits function)
"""

import math
import os
import random
import re
import sys

DEBUG = False
SORT = True

#
# Complete the 'getMaximumOutfits' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY outfits
#  2. INTEGER money
#

# def getMaximumOutfits(outfits, money):
# 	for i,o in enumerate(outfits):
# 		print("%(money)s - %(o)s"%vars())
# 		if o > money:
# 			return i
# 		money -= o
# 	
# 	return len(outfits)

def getMaximumOutfits(outfits, money):
	if SORT:
		outfits.sort()
	
	bought = 0
	for i, o in enumerate(outfits):
		if money <= 0:
			return bought
		
		if money >= o:
			if DEBUG: print("%(money)s - %(o)s (BOUGHT!)" % vars())
			bought += 1
			money -= o
		else:
			if DEBUG: print("%(money)s - %(o)s" % vars())
		
	return bought

def test():
	global DEBUG
	DEBUG = True
	
	print(">>>> %s <<<<" % getMaximumOutfits(
		[1,5,5,2,2,2,1,1,1],
		10
	))
	
	print(">>>> %s <<<<" % getMaximumOutfits(
		[1, 5, 5, 2, 2, 2, 1, 1, 1],
		1
	))
	
	# print(">>>> %s <<<<" % getMaximumOutfits(
	# 	[10,10,10],
	# 	5
	# ))
	
	print(">>>> %s <<<<" % getMaximumOutfits(
		[],
		10
	))

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	outfits_count = int(input().strip())
	
	outfits = []
	
	for _ in range(outfits_count):
		outfits_item = int(input().strip())
		outfits.append(outfits_item)
	
	money = int(input().strip())
	
	result = getMaximumOutfits(outfits, money)
	
	fptr.write(str(result) + '\n')
	
	fptr.close()


if __name__ == '__main__':
	#test()
	main()
