#!/usr/bin/python

import sys

suffix = 0

for line in sys.stdin:
	if line[0] == '@':
		# header line
		print(line[:-1])
		continue
	fields = line.split()
	fields[0] = fields[0] + '_' + str(suffix)
	print('\t'.join(fields))
	suffix += 1
