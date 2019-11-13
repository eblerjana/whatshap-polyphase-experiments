#!/usr/bin/python

import sys

for line in sys.stdin:
	if line[0] == '@':
		# header line
		print(line[:-1])
		continue
	fields = line.split()
	if fields[9] == '*':
		print(line[:-1])
		continue
	assert fields[10] == '*'
	seq_len = len(fields[9])
	# use default base quality of 40
	default_qual = '5' * seq_len
	fields[10] = default_qual
	print('\t'.join(fields))
