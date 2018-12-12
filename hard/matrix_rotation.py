#!/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.hackerrank.com/challenges/matrix-rotation-algo/problem

Time: 3h
"""

import random

def next_pos(m,n,y,x):
	# Up
	if y == 0:
		if x == 0:
			return (1, 0)
		else:
			return (0, x-1)
	
	# Left
	if x == 0:
		if y == m-1:
			return (m-1, 1)
		else:
			return (y+1, 0)
		
	# Down
	if y == m-1:
		if x == n-1:
			return (y-1, x)
		else:
			return (y, x+1)
	
	# Right
	if x == n-1:
		if y == 0:
			return (0, x-1)
		else:
			return (y-1, x)

	raise Exception("no! m=%(m)s, n=%(n)s, y=%(y)s, x=%(x)s")


def print_matrix(matrix):
	for row in matrix:
		print(" ".join(map(str,row)), flush=True)
	
def reduce_r(r, current_m, current_n):
	cycle_len = current_m*2 + (current_n-2)*2
	return r % cycle_len

def matrixRotation(matrix, r):
	m = len(matrix)
	n = len(matrix[0])
	
	new_matrix = [[None for x in range(0, n)] for y in range(0, m)]
	
	starting_y, starting_x = 0, 0
	current_m, current_n = m, n
	while (starting_y < m // 2) and (starting_x < n // 2):
		y, x = starting_y, starting_x
		
		# Let's reduce r to skip useless cycles (when r is very big)
		reduced_r = reduce_r(r, current_m, current_n)
		
		# Calculating where the first element will ends up, based on r.
		new_start_pos_y, new_start_pos_x = y - starting_y, x - starting_x
		for i in range(0, reduced_r):
			new_start_pos_y, new_start_pos_x = next_pos(current_m, current_n, new_start_pos_y, new_start_pos_x)
		
		new_start_pos_y, new_start_pos_x = new_start_pos_y + starting_y, new_start_pos_x + starting_x
		new_pos_y, new_pos_x = new_start_pos_y, new_start_pos_x
		
		first_pass = True
		
		# Cycling for all elements in this matrix ring. We have two positions, the starting pos and the arrival pos.
		# For every cycle we shift both 1 element forth (in order to spare useless calculation when matrix is big)
		while first_pass or y != starting_y or x != starting_x:
			first_pass = False
			
			new_matrix[new_pos_y][new_pos_x] = matrix[y][x]
			
			# Next starting pos
			y, x = next_pos(current_m, current_n, y-starting_y, x-starting_x)
			y, x = y + starting_y, x + starting_x
			
			# Next arrival pos
			new_pos_y, new_pos_x = next_pos(current_m, current_n, new_pos_y - starting_y, new_pos_x - starting_x)
			new_pos_y, new_pos_x = new_pos_y + starting_y, new_pos_x + starting_x
		
		# Let's going deeper at next matrix ring
		starting_y, starting_x = starting_y + 1, starting_x + 1
		current_m, current_n = current_m - 2, current_n - 2
	
	print_matrix(new_matrix)

def apply_to_random_matrix(m, n, r):
	import time
	matrix = [[random.randint(1, 10) for x in range(0, n)] for y in range(0, m)]
	startts = time.time()
	matrixRotation(matrix, r)
	print("Took %.2f sec" % (time.time()-startts))

if __name__ == '__main__':
	mnr = input().rstrip().split()

	m = int(mnr[0])
	n = int(mnr[1])
	r = int(mnr[2])

	matrix = []

	for _ in range(m):
		matrix.append(list(map(int, input().rstrip().split())))

	matrixRotation(matrix, r)
	
	# Target
	#apply_to_random_matrix(300, 300, 999999999)
	
