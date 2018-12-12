# !/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.hackerrank.com/challenges/climbing-the-leaderboard/problem

Time: 47 min
"""

import math
import os
import sys
import random
import re
import sys

def enumerate_reversed(L):
   for index in reversed(range(len(L)-1, -1, -1)):
      yield index, L[index]

# Complete the climbingLeaderboard function below.
def climbingLeaderboard(scores, alice):
	current_rank = 0
	current_score = 10**9 + 1
	
	current_alice_pos = len(alice)-1
	
	alice_ranks = [None for i in range(0,len(alice))]
	
	for s in scores:
		if s < current_score:
			current_rank += 1
			current_score = s
			
		while current_alice_pos >= 0 and alice[current_alice_pos] >= current_score:
			alice_ranks[current_alice_pos] = current_rank
			current_alice_pos -= 1
	
	current_rank += 1
	while current_alice_pos >= 0:
		alice_ranks[current_alice_pos] = current_rank
		current_alice_pos -= 1
	
	return alice_ranks


if __name__ == '__main__':
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	scores_count = int(input())
	
	scores = list(map(int, input().rstrip().split()))
	
	alice_count = int(input())
	
	alice = list(map(int, input().rstrip().split()))
	
	result = climbingLeaderboard(scores, alice)
	
	fptr.write('\n'.join(map(str, result)))
	fptr.write('\n')
	
	fptr.close()
