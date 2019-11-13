import sys
import re

for line in sys.stdin:
	fields = re.split("[:-]", line)
#	fields = line.split(':', '-')[0]
	chrom = fields[0]
	start = fields[1]
	end = fields[2][:-1]
	print('\t'.join([chrom,start,end]))
