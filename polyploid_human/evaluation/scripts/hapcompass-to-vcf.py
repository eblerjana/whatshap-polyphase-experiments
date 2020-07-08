import sys
import argparse
import datetime

parser = argparse.ArgumentParser(prog='hapcompass-to-vcf.py', description=__doc__)
parser.add_argument('txt', metavar='FILE', help='hapcompass file (OUTPUT_PREFIX_<ALGORITHM>_solution.txt)')
parser.add_argument('vcf', metavar='VCF', help='VCF file containing the unphased variants')
args = parser.parse_args()

variants_to_phasing = {}

block_id = 0
# read the hapcompass input
for line in open(args.txt, 'r'):
	if line[0:5] == 'BLOCK':
		block_id += 1
		continue
	splitted = line.split()
	if splitted == []:
		continue
	variants_to_phasing[splitted[1]] = (block_id, splitted[3:])


# write the phased vcf
for line in open(args.vcf, 'r'):
	if line[0] == '#':
		print(line[:-1])
		continue
	splitted = line.split()
	splitted[8] = 'GT:PS'
	splitted[9] = '.:.'
	if splitted[1] in variants_to_phasing:
		phasing = variants_to_phasing[splitted[1]]
		splitted[9] = '|'.join(phasing[1]) + ':' + str(phasing[0])
	print('\t'.join(splitted))
