#!/bin/python3
# -*- coding: utf-8 -*-

"""
NOT FINISHED
Time: 13m
"""

import math
import os
import random
import re
import sys



#
# Complete the 'getMaximumOutfits' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY outfits
#  2. INTEGER money
#

def getMaximumOutfits(outfits, money):
	for i,o in enumerate(outfits):
		print("%(money)s - %(o)s"%vars())
		if o > money:
			return i
		money -= o
	
	return len(outfits)

if __name__ == '__main__':
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
