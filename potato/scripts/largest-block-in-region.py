import sys
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(prog='largest-block-in-region.py', description=__doc__)
parser.add_argument('region', metavar='REGION', help='region for which to extract the largest phasing block.')
args = parser.parse_args()

block_to_lines = defaultdict(list)

region_chrom = args.region.split(':')[0]
region_start = int(args.region.split(':')[1].split('-')[0])
region_end = int(args.region.split(':')[1].split('-')[1])

for line in sys.stdin:
	if line.startswith('#'):
		# header line
		print(line[:-1])
		continue

	fields = line.split()
	chrom = fields[0]
	start = int(fields[1])

	if chrom != region_chrom:
		continue
	if start < region_start or start > region_end:
		continue

	# get block id
	format = fields[8].split(':')
	sample = fields[9].split(':')
	genotype = sample[format.index('GT')]
	if '|' in genotype:
		assert 'PS' in format
		block_id = sample[format.index('PS')]
		block_to_lines[block_id].append(line[:-1])

# print lines corresponding to longest block
max_block_len = 0
max_block_id = None
for block, variants in block_to_lines.items():
	if len(variants) >= max_block_len:
		max_block_len = len(variants)
		max_block_id = block

for line in block_to_lines[max_block_id]:
	print(line)
	
