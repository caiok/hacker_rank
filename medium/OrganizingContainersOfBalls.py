#!/bin/python3
#  -*- coding: utf-8 -*-

"""
https://www.hackerrank.com/challenges/organizing-containers-of-balls/problem

Result: 30 / 30

Time: 5m + 1h20m + 2h20m + 1h = 5h


The hackerank solution seems wrong to me, I left this message in the discussion:

	**The proposed solution seems wrong to me.**
	
	I think this matrix demonstrates the issue:
	```
	[[0, 2, 0],
	 [1, 1, 1],
	 [2, 0, 1]]
	```
	
	After some swaps we can arrive to:
	```
	[[2, 0, 0],
	 [0, 3, 0],
	 [1, 0, 2]]
	```

	Where we got stuck. I think the failure is due to the fact that the two lists produced by summing
	up rows and columns become [2, 3, 3] and [3, 3, 2], that sorted are indentical, but these 3s are
	not the same thing ;-)
	
	I fear that **the test cases were produced with this wrong assumption in mind**, since my code
	works well with a atrix generated randomly swapping starting from a correct final matrix, but doesn't
	work in a lot of tests of this exercise.
	
	And vice versa, if in the final random swapped matrix I add a ball somewhere (not in a matrix cell
	where x = y obviously), my codes print "Impossible", whether the solution print "Possible" (the
	matrix above is an example)
"""

import math
import os
import sys
import random

from pprint import pprint
from copy import deepcopy

DEBUG = True

# ---------------------------------------- #


def hom_many_must_transfer(containers, my_type):
	"""
	
	:param containers: the containers matrix
	:param my_type: type of this container (and its position in the matrix)
	:return: how many elements not belonging to this type the container must transfer to other containers
	"""
	
	c = 0
	for type, n in enumerate(containers[my_type]):
		if type == my_type:
			continue
		c += n
	return c


def hom_many_must_receive(containers, my_type):
	"""

	:param containers: the containers matrix
	:param my_type: type of this container (and its position in the matrix)
	:return: how many elements not belonging to this type the container must transfer to other containers
	"""
	
	c = 0
	for i in range(len(containers)):
		if i == my_type:
			continue
		c += containers[i][my_type]
	return c

# ---------------------------------------- #


def retrieve_all(containers, my_index, target_index):
	"""
	Retrieve all other container balls belonging to this container, transferring to it other balls types
	
	:param containers: container_matrix
	:param my_index: this container index (and type)
	:param target_index: target container index
	:return: True if the transfer was successful, False otherwise
	"""
	
	i = 0
	how_many_retrievable = containers[target_index][my_index]
	
	while i < len(containers) and how_many_retrievable > 0:
		if i == my_index:
			i += 1
			continue
		
		to_retrieve = min(how_many_retrievable, containers[my_index][i])
		
		containers[target_index][my_index] -= to_retrieve
		containers[my_index][my_index] += to_retrieve
		
		containers[target_index][i] += to_retrieve
		containers[my_index][i] -= to_retrieve
		
		how_many_retrievable -= to_retrieve
		i += 1
		
	return how_many_retrievable == 0


def are_containers_finished(containers):
	for i in range(len(containers)):
		for j in range(len(containers)):
			if i != j and containers[i][j] > 0:
				return False
	
	return True

def organizingContainers_mine(containers):
	# Input:
	#   containers[container][type] = how_many
	
	for i in range(len(containers)):
		
		for j in range(i + 1, len(containers)):
			done = retrieve_all(containers, i, j)
			if not done:
				#print("i=%s, j=%s" % (i, j))
				#pprint(containers)
				return "Impossible"
	
	#pprint(containers)
	
	if are_containers_finished(containers):
		return "Possible"
	else:
		return "Impossible"

# ---------------------------------------- #


def organizingContainers_official(containers):
	# Input:
	#   containers[container][type] = how_many
	
	containers_count = [sum(c) for c in containers]
	types_count = []
	for i in range(len(containers)):
		c = 0
		for j in range(len(containers)):
			c += containers[j][i]
		types_count.append(c)
	
	containers_count.sort()
	types_count.sort()
	
	if containers_count == types_count:
		return "Possible"
	else:
		return "Impossible"
	
# ---------------------------------------- #


def test():
	# print(organizingContainers([
	# 	[1, 2, 3, 4],
	# 	[2, 5, 12, 0],
	# 	[4, 4, 4, 4],
	# 	[0, 1, 2, 3]
	# ]))
	
	# print(organizingContainers([
	# 	[0, 2, 1],
	# 	[1, 1, 1],
	# 	[2, 0, 0],
	# ]))
	
	#672
	
	seed = random.randint(0, 1000)
	print("Seed %s" % seed)
	random.seed(seed)
	
	for i in range(100):
		assert_possible(3, 0)
		assert_possible(3, 1)

def assert_possible(n, n_errors):
	containers = add_randomly_to_matrix(generate_matrix_randomly(n), n_errors)
	res1 = organizingContainers_mine(deepcopy(containers))
	res2 = organizingContainers_official(deepcopy(containers))
	res_correct = "Possible" if n_errors == 0 else "Impossible"
	
	pprint(containers)
	print("res1=%(res1)s, res2=%(res2)s, res_correct=%(res_correct)s" % vars())
	if res1 != res2:
		raise Exception("INCOHERENT!")
	if res1 != res_correct:
		raise Exception("Problem")


# ---------------------------------------- #


def random_non_empty_index(container):
	while True:
		i = random.randint(0, len(container) - 1)
		if container[i] > 0:
			return i

def generate_matrix_randomly(n):
	stub = [0] * n
	containers = []
	for i in range(n):
		container = list(stub)
		container[i] = random.randint(1, 5)
		containers.append(container)
	
	pprint(containers)
	orig_sum = sum([sum(c) for c in containers])
	
	for _ in range(100):
		src = containers[random.randint(0, n - 1)]
		dst = containers[random.randint(0, n - 1)]
		while dst == src:
			dst = containers[random.randint(0, n - 1)]
		
		x = random_non_empty_index(src)
		y = random_non_empty_index(dst)
		#print(x, y)
		src[x] -= 1
		dst[x] += 1
		dst[y] -= 1
		src[y] += 1
		#pprint(containers)
	
	pprint(containers)
	final_sum = sum([sum(c) for c in containers])
	assert final_sum == orig_sum
	
	return containers

def add_randomly_to_matrix(containers, n):
	x = random.randint(0, len(containers) - 1)
	y = random.randint(0, len(containers) - 1)
	while x == y:
		y = random.randint(0, len(containers) - 1)
	containers[x][y] += n
	return containers

# ---------------------------------------- #


if __name__ == '__main__':
	#test()
	#sys.exit()
	
	fptr = open(os.environ['OUTPUT_PATH'], 'w')

	q = int(input())

	for q_itr in range(q):
		n = int(input())

		container = []

		for _ in range(n):
			container.append(list(map(int, input().rstrip().split())))

		result = organizingContainers_mine(container)

		fptr.write(result + '\n')

	fptr.close()
