#!/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.hackerrank.com/challenges/encryption/problem

Time: 25m
"""

import math
import os
import random
import re
import sys

# ===================================================================== #

# Complete the encryption function below.
def encryption(s):
	s = s.replace(" ", "")
	
	low = math.floor(math.sqrt(len(s)))
	high = math.ceil(math.sqrt(len(s)))
	
	rows = low
	cols = high
	
	matrix = []
	for x in range(0, len(s), cols):
		matrix.append(s[x:x+cols])
	
	print(matrix)
	
	encoded = []
	for c in range(0, cols):
		ss = ""
		for r in range(0,len(matrix)):
			if c < len(matrix[r]):
				ss += matrix[r][c]
		encoded.append(ss)
	
	return " ".join(encoded)

# ===================================================================== #

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout


	s = input()
	
	result = encryption(s)
	
	fptr.write(result + '\n')
	
	fptr.close()

if __name__ == '__main__':
	main()
