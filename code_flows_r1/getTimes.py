#!/bin/python3
#  -*- coding: utf-8 -*-

import math
import os
import random
import re
import sys

DEBUG = False

# =========================================================================== #

def add_to_queue(t:int, i:int, dir:str, enter_queue:list, exit_queue:list) -> None:
	if dir == 1:
		if DEBUG: print("t = %(t)2s: [exit] Add %(i)s" % vars())
		exit_queue.append(i)
	else:
		if DEBUG: print("t = %(t)2s: [enter] Add %(i)s" % vars())
		enter_queue.append(i)

# --------------------------------------------------------------------------- #

#
# Complete the 'getTimes' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER_ARRAY time
#  2. INTEGER_ARRAY direction
#

def getTimes(time, direction):
	n = len(time)
	
	enter_queue = []
	exit_queue = []
	
	i = 0
	t = 0
	forward_t = 0
	current_dir = ""
	
	turnstile_pass = [None] * n # (pre-allocation)
	
	if DEBUG:
		print(time)
		print(direction)
	
	# Leap cycle: every cycle is a leap in the time ticks
	while i < n:
		t = time[i]
		current_dir = ''
		if DEBUG: print("t = %(t)2s: (Leap forward)" % vars())
		
		add_to_queue(t, i, direction[i], enter_queue, exit_queue)
		i += 1
		
		# Tick cycle: every cycle is a time "tick"
		something_happened = False
		while something_happened or enter_queue or exit_queue:
			
			something_happened = False
			
			# Get in cycle: add to the appropriate queue all people arrived until now
			while i < n and time[i] <= t:
				add_to_queue(t, i, direction[i], enter_queue, exit_queue)
				i += 1
				
			if DEBUG: print("t = %(t)2s: enter=%(enter_queue)s, exit=%(exit_queue)s" % vars())
			
			if current_dir == '':
				if enter_queue and exit_queue:
					current_dir = 'exit'
					if DEBUG: print("t = %(t)2s: [direction] conflict! starting with EXIT" % vars())
				elif exit_queue:
					current_dir = 'exit'
					if DEBUG: print("t = %(t)2s: [direction] starting with EXIT" % vars())
				elif enter_queue:
					current_dir = 'enter'
					if DEBUG: print("t = %(t)2s: [direction] starting with ENTER" % vars())
				
			if current_dir == 'exit':
				if exit_queue:
					curr_i = exit_queue.pop(0)
					turnstile_pass[curr_i] = t
					something_happened = True
					if DEBUG: print("t = %(t)2s: [exit] %(curr_i)s exited" % vars())
					t += 1
					continue
				else:
					if enter_queue:
						current_dir = 'enter'
						if DEBUG: print("t = %(t)2s: [direction] exits finished, switch to ENTER" % vars())
					else:
						current_dir = ''
						if DEBUG: print("t = %(t)2s: [direction] exits finished, switch to >NONE<" % vars())
				
			if current_dir == 'enter':
				if enter_queue:
					curr_i = enter_queue.pop(0)
					turnstile_pass[curr_i] = t
					something_happened = True
					if DEBUG: print("t = %(t)2s: [enter] %(curr_i)s entered" % vars())
					t += 1
					continue
				else:
					if exit_queue:
						current_dir = 'exit'
						if DEBUG: print("t = %(t)2s: [direction] enters finished, switch to EXIT" % vars())
					else:
						current_dir = ''
						if DEBUG: print("t = %(t)2s: [direction] enters finished, switch to >NONE<" % vars())
	
	return turnstile_pass

# =========================================================================== #

def test():
	global DEBUG
	DEBUG = True
	
	# print(">>>> %s <<<<" % getTimes(
	# 	[  5,  5,  5,  6,  6,  7, 10, 15, 15, 16], 
	# 	[  1,  0,  1,  0,  0,  0,  1,  0,  1,  1])
	# )
	
	print(">>>> %s <<<<" % getTimes(
		[  0,  1,  1,  3,  3],
		[  0,  1,  0,  0,  1])
	)

5
0
1
1
3
3
5
0
1
0
0
1

# --------------------------------------------------------------------------- #

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout

	time_count = int(input().strip())

	time = []

	for _ in range(time_count):
		time_item = int(input().strip())
		time.append(time_item)

	direction_count = int(input().strip())

	direction = []

	for _ in range(direction_count):
		direction_item = int(input().strip())
		direction.append(direction_item)

	result = getTimes(time, direction)

	fptr.write('\n'.join(map(str, result)))
	fptr.write('\n')

	fptr.close()

# --------------------------------------------------------------------------- #

if __name__ == '__main__':
	test()
	#main()
