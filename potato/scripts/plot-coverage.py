import sys
import argparse
import math
import numpy
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(prog='plot-coverage.py', description=__doc__)
parser.add_argument('output', metavar='OUTPUT', help='name of output file')
args = parser.parse_args()

max_val = 600

title = args.output.split('.')[-2]

all_coverages = []

for line in sys.stdin:
	fields = line.split()
	coverage = int(fields[2])
	if coverage > max_val:
		continue
	all_coverages.append(coverage)

plt.hist(all_coverages, bins=100)
plt.xlim(0, max_val)
plt.ylim(0, 14000000)
plt.title(title)
plt.xlabel('Coverage')
plt.ylabel('Count')
plt.savefig(args.output)
