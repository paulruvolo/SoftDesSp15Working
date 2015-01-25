#!/usr/bin/env python

""" A sample implementation of the file_counter component of the fileio tool """

import os
import sys

def update_counter(file_name, reset=False):
	""" Updates a counter stored in the file 'file_name'

		A new counter will be created and initialized to 1 if none exists.
		If the counter already exists, the counters value will be incremented
		returns: the new counter value

	>>> update_counter('blah.txt',True)
	1
	>>> update_counter('blah.txt')
	2
	>>> update_counter('blah2.txt',True)
	1
	>>> update_counter('blah.txt')
	3
	>>> update_counter('blah2.txt')
	2
	"""
	if os.path.exists(file_name) and not(reset):
		try:
			f = open(file_name,'r')
		except:
			print "Unexpected error!"
			return
		for line in f:
			current_val = int(line)
		f.close()
		try:
			f = open(file_name,'wt')
		except:
			print "Unexpected error!"
			return
	else:
		try:
			f = open(file_name,'wt')
		except:
			print "Unexpected error!"
			return
		current_val = 0
	current_val += 1
	f.write(str(current_val)+"\n")
	f.close()
	return current_val


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "USAGE: python fileio_tool.py file-name"
	else:
		print "new value is " + str(update_counter(sys.argv[1]))