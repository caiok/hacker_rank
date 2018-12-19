#!/bin/python3
#  -*- coding: utf-8 -*-

"""
Points: 75
Result: 11/14

Time: 6h
"""

import math
import os
import random
import re
import sys


DEBUG = False

MAX_TRIALS = 10**5 + 1

# =========================================================================== #

class Element(object):
	start_t: int = None
	end_t: int = None
	prev = None
	next = None
	
	def __init__(self, start_t, end_t):
		self.start_t = start_t
		self.end_t = end_t

# --------------------------------------------------------------------------- #

class Break(Element):
	duration:int = None
	
	def __init__(self, duration, start_t, end_t):
		super(Break, self).__init__(start_t, end_t)
		self.duration = duration
	
	def __str__(self):
		return "b%s" % self.duration
	
	def __repr__(self):
		return "b%s(%s-%s)" % (self.duration, self.start_t, self.end_t)

# --------------------------------------------------------------------------- #

class Presentations(Element):
	howmany:int = None
	
	def __init__(self, howmany, start_t, end_t):
		super(Presentations, self).__init__(start_t, end_t)
		self.howmany = howmany
		#print("homany=%s start=%s,end=%s"%(self.howmany,self.start_t, self.end_t))
	
	def __str__(self):
		return "p%s" % self.howmany
	
	def __repr__(self):
		return "p%s(%s-%s)" % (self.howmany, self.start_t, self.end_t)
	
	def add(self, end_t):
		assert end_t > self.end_t
		self.howmany += 1
		self.end_t = end_t
		#print("> homany=%s end=%s"%(self.howmany,self.end_t))

# =========================================================================== #

class TimeLine(object):
	first: Element = None
	last: Element = None
	first_break: Break = None
	last_break: Break = None
	
	k = 0
	
	total_breaks = 0
	total_breaks_time = 0
	total_presentations_time = 0
	
	max_break_time = 0
	min_presentations_time = 99999999
	
	breaks_list = []
	
	def __str__(self):
		s = ""
		curr_el = self.first
		while curr_el != None:
			s += str(curr_el)
			curr_el = curr_el.next
		return s
	
	def __repr__(self):
		s = "-------------------------\n"
		curr_el = self.first
		while curr_el != None:
			s += repr(curr_el) + " "
			curr_el = curr_el.next
		s += "\n"
		s += "-------------------------\n"
		s += "first: %r\n" % self.first
		s += "last: %r\n" % self.last
		s += "first_break: %r\n" % self.first_break
		s += "last_break: %r\n" % self.last_break
		s += "\n"
		s += "k: %r\n" % self.k
		s += "total_breaks: %r\n" % self.total_breaks
		s += "total_breaks_time: %r\n" % self.total_breaks_time
		s += "total_presentations_time: %r\n" % self.total_presentations_time
		s += "max_break_time: %r\n" % self.max_break_time
		s += "min_presentations_time: %r\n" % self.min_presentations_time
		s += "-------------------------\n"
		return s
	
	def add_element(self, el):
		if self.first == None:
			self.first = el
			self.last = el
		else:
			self.last.next = el
			el.prev = self.last
			self.last = el
		
		if type(el) is Break:
			if self.first_break == None:
				self.first_break = el
			self.last_break = el
			self.total_breaks += 1
			self.total_breaks_time += el.duration
			self.max_break_time = max(self.max_break_time, el.duration)
			self.breaks_list.append(el)
		else:
			self.total_presentations_time += el.howmany
			self.min_presentations_time = min(self.min_presentations_time, el.howmany)
	
	# WARNING: does really time start from 0?
	def init(self, n, t, start, finish, k):
		self.k = k
		
		tx = 0
		i = 0
		
		curr_pres = None
		while tx < t and i < n:
			if start[i] > tx:
				if curr_pres:
					self.add_element(curr_pres)
					curr_pres = None
				self.add_element(Break(start[i]-tx, tx, start[i]))
			
			if not curr_pres:
				curr_pres = Presentations(1, start[i], finish[i])
			else:
				curr_pres.add(finish[i])
			
			tx = finish[i]
			i += 1
		
		if curr_pres:
			self.add_element(curr_pres)
			curr_pres = None
		
		if tx < t:
			self.add_element(Break(t-tx, tx, t))
			
	def explore(self) -> int:
		if self.k >= self.total_presentations_time:
			if DEBUG: print("Early exit for k > total_presentations_time")
			return self.total_breaks_time # We can already exit
		
		if self.k < self.min_presentations_time:
			if DEBUG: print("Early exit for k < min_presentations_time")
			return self.max_break_time # We can already exit
		
		max_breaks_time = 0
		
		# curr_break = self.first_break
		# while curr_break != None:
		# 	if DEBUG: print("> %s" % curr_break)
		# 	cog = CenterOfGravity(self, curr_break, self.k)
		# 	btime = cog.explore()
		# 
		# 	if btime == self.total_breaks_time:
		# 		if DEBUG: print("Early exit for btime = total_breaks_time")
		# 		return self.total_breaks_time # We can already exit
		# 
		# 	if btime > max_breaks_time:
		# 		max_breaks_time = btime
		# 
		# 	if curr_break.next:
		# 		curr_break = curr_break.next.next
		# 	else:
		# 		break
		
		# If there are too many breaks we have to limits our trials by ordering all breaks for their respective 
		# duration and then executing our algorithm only for the first MAX_TRIALS
		if self.total_breaks > MAX_TRIALS:
			self.breaks_list.sort(key=lambda x: x.duration, reverse=True)
		
		for i,curr_break in enumerate(self.breaks_list):
			if i > MAX_TRIALS:
				if DEBUG: print("Break after %s trials"%MAX_TRIALS)
				return max_breaks_time
			
			if DEBUG: print("> %s" % curr_break)
			cog = CenterOfGravity(self, curr_break, self.k)
			btime = cog.explore()

			if btime == self.total_breaks_time:
				if DEBUG: print("Early exit for btime = total_breaks_time")
				return self.total_breaks_time  # We can already exit

			if btime > max_breaks_time:
				max_breaks_time = btime
		
		return max_breaks_time

# --------------------------------------------------------------------------- #

class CenterOfGravity(object):
	"""
	We take every single break in the timeline and explore how much break duration we can achieve collapsing
	nearby breaks with k "spending capacity".
	We consider all contiguous presentations as a single entity of weight "h" where h is the number of presentations.
	When we want to join two breaks separated by h presentations we need to reschedule all these presentations at once.
	Notice: After a presentation (and all its nearby companions) has been rescheduled, it can be moved everywhere
	(without changing che presentations order), so after we spend h in order to move a group of presentations we can
	merely make them "disappear". 
	
	In order to simplify things we start from our center and "eat" presentations in order to merge breaks and we
	keep pointers to the left-most break that we merged (prev_center) and the right-most one (next_center) accumulating
	the total break_time and decreasing remaining_k.
	Notice: which direction we choose is subjective and in order to achieve the "best" results we should try every
	combination. We follow a somewhat greedy approach and when we have to choose left (prev) or right (next) we 
	consider the highest cost of the two and then we consider what we can achieve "eating" in the other direction
	with the same cost. We than compare the obtained break size and choose which direction to follow.
	
	Ex: in the left we have a bunch of 5 presentations then a break of 3 slots, on the right we have a sequence of
	2 presentations, than a break of 2 slots, 2 presentations and so on. We choose to move on the right because with a
	max spending of 5 we can achieve a break of 4 instead of one of 3.
	"""
	
	timeline:TimeLine = None
	prev_center: Break = None
	next_center: Break = None
	break_time: int = None
	
	remaining_k: int = None
	spent_k: int = 0
	
	def __init__(self, timeline:TimeLine, center:Break, k:int):
		self.timeline = timeline
		self.prev_center = center
		self.next_center = center
		self.remaining_k = k
		self.break_time = center.duration
	
	def explore_next(self, curr: Presentations, max_k: int) -> int:
		value = 0
		while max_k > curr.howmany:
			max_k -= curr.howmany
			value += curr.next.duration
			if curr.next == self.timeline.last_break:
				return value
			curr = curr.next.next
		return value
	
	def explore_prev(self, curr: Presentations, max_k: int) -> int:
		value = 0
		while max_k > curr.howmany:
			max_k -= curr.howmany
			value += curr.prev.duration
			if curr.prev == self.timeline.first_break:
				return value
			curr = curr.prev.prev
		return value
	
	def can_go_prev(self, b:Break):
		if b == self.timeline.first_break:
			return False
		if b.prev.howmany > self.remaining_k:
			return False
		return True
	
	def can_go_next(self, b:Break):
		if b == self.timeline.last_break:
			return False
		if b.next.howmany > self.remaining_k:
			return False
		return True
	
	def choose_direction(self) -> (int,str):
		
		# Check if is not the first / last or if we have enough k to follow the link
		if not self.can_go_prev(self.prev_center) and not self.can_go_next(self.next_center):
			return (0, "x")
		if not self.can_go_prev(self.prev_center):
			return (0, ">")
		if not self.can_go_next(self.next_center):
			return (0, "<")
		
		# Now we make some deeper checks
		if self.prev_center.prev.howmany == self.next_center.next.howmany:
			if self.prev_center.prev.prev.duration >= self.next_center.next.next.duration:
				return (0, "<")
			else:
				return (0, ">")
		if self.prev_center.prev.howmany > self.next_center.next.howmany:
			max_cost = self.prev_center.prev.howmany
			next_value = self.explore_next(self.next_center.next, max_cost)
			if self.prev_center.prev.prev.duration > next_value or max_cost:
				return 0, "<"
			else:
				return max_cost, ">"
		else:
			max_cost = self.next_center.next.howmany
			prev_value = self.explore_prev(self.prev_center.prev, max_cost)
			if self.next_center.next.next.duration > prev_value or max_cost:
				return 0, ">"
			else:
				return max_cost, "<"
	
	def go_next(self):
		spent_k = self.next_center.next.howmany
		self.remaining_k -= spent_k
		self.spent_k += spent_k
		
		self.next_center = self.next_center.next.next
		self.break_time += self.next_center.duration
	
	def go_prev(self):
		spent_k = self.prev_center.prev.howmany
		self.remaining_k -= spent_k
		self.spent_k += spent_k
		
		self.prev_center = self.prev_center.prev.prev
		self.break_time += self.prev_center.duration
	
	def explore(self) -> int:
		"""
		:return: how many slots of contiguous break we can achieve using this break as "center of gravity"
		"""
		
		while self.remaining_k > 0 or self.break_time == self.timeline.total_breaks_time:
			
			max_cost, direction = self.choose_direction()
			if DEBUG: print("%s<->%s (b:%s, r:%s) :: %s" % (self.prev_center,self.next_center,self.break_time,self.remaining_k,direction))
			if direction == "x":
				return self.break_time
			elif direction == "<":
				self.go_prev()
			elif direction == ">":
				self.go_next()
			else:
				raise Exception("what? %s" % direction)
		
		return self.break_time

# =========================================================================== #

#
# Complete the 'findBreakDuration' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER k
#  3. INTEGER t
#  4. INTEGER_ARRAY start
#  5. INTEGER_ARRAY finish
#

def findBreakDuration(n, k, t, start, finish):
	timeline = TimeLine()
	timeline.init(n, t, start, finish, k)
	if DEBUG: print(repr(timeline))
	return timeline.explore()

# =========================================================================== #

def main():
	fptr = None
	if ('OUTPUT_PATH' in os.environ):
		fptr = open(os.environ['OUTPUT_PATH'], 'w')
	else:
		fptr = sys.stdout
	
	n = int(input().strip())
	
	k = int(input().strip())
	
	t = int(input().strip())
	
	start_count = int(input().strip())
	
	start = []
	
	for _ in range(start_count):
		start_item = int(input().strip())
		start.append(start_item)
	
	finish_count = int(input().strip())
	
	finish = []
	
	for _ in range(finish_count):
		finish_item = int(input().strip())
		finish.append(finish_item)
	
	result = findBreakDuration(n, k, t, start, finish)
	
	fptr.write(str(result) + '\n')
	
	fptr.close()

# --------------------------------------------------------------------------- #

def test():
	global DEBUG
	DEBUG = True
	
	# n, k, t, start, finish
	pres = [
		(1,2),(2,3), 
		(5,6),(6,7), 
		(10,11),(11,12),(12,13),(13,14)
	]
	ret = findBreakDuration(len(pres), 4, 18, *zip(*pres))
	print(">>> %s <<<" % ret)
	
	# n, k, t, start, finish
	# pres = [
	# 	(1,3),
	# 	(5,7),
	# 	(10,14)
	# ]
	# ret = findBreakDuration(len(pres), 3, 18, *zip(*pres))
	# print(">>> %s <<<" % ret)

# --------------------------------------------------------------------------- #

if __name__ == '__main__':
	test()
	#main()

