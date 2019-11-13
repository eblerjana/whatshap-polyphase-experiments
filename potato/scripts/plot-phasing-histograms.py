import argparse
import numpy
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(prog='plot-phasing-histograms.py', description=__doc__)
parser.add_argument('tsv', metavar='TSV', help='tsv output produced by whatshap stats.')
parser.add_argument('--output', '-o', default='histograms', help='name of the output file.')
parser.add_argument('--only-intervals', default=False, action='store_true', help='consider only bed intervals.')
args = parser.parse_args()

block_lengths = []
phased_in_longest = []
genes_phased = 0
total = 0
total_phasable = 0

for line in open(args.tsv, 'r'):
	if line[0] == '#':
		# header line
		continue
	fields = line.split()
	if args.only_intervals:
		if not ':' in fields[1]:
			continue

	# determine number of phased blocks
	nr_blocks = int(fields[7])
	total += 1
	if nr_blocks > 0:
		genes_phased += 1
		block_lengths.append(nr_blocks)

	# total number of het variants in interval
	het_vars = float(fields[18])
	phased_vars = float(fields[11])
	if het_vars > 0:
		total_phasable += 1

		# determine fraction of phased variants in longest block
		phased_in_longest.append ( (phased_vars / het_vars) * 100.0 )
	else:
		assert phased_vars == 0

assert len(phased_in_longest) == total_phasable

# print some statistics
one_block = block_lengths.count(1)
print('------------ Interval statistics ------------')
print('total number of intervals:\t' + str(total))
print('intervals with any heterozygous variants:\t' + str(total_phasable) )

print('------------ Block number statistics ------------')
print('phased intervals:\t' + str(genes_phased) + ' / ' + str(total_phasable) + ' (' + str(genes_phased / float(total_phasable)) + ')')
print('phased in one block:\t' + str(one_block) + ' / ' + str(total_phasable) + ' (' + str(one_block / float(total_phasable)) + ')')
print('max number of blocks per phased interval:\t' + str(max(block_lengths)))
print('average number of blocks per phased interval:\t' + str(numpy.mean(block_lengths)))

print('------------ Longest block statistics ------------')
more_50 = sum(i >= 50 for i in phased_in_longest)
print('intervals in which longest phased block covered >= 50% of all variants:\t' + str(more_50) + ' / ' + str(total_phasable) + ' (' + str(more_50 / float(total_phasable)) + ')')
more_90 = sum(i >= 90 for i in phased_in_longest)
print('intervals in which longest phased block covered >= 90% of all variants:\t' + str(more_90) + ' / ' + str(total_phasable) + ' (' + str(more_90 / float(total_phasable)) + ')')
all_phased = sum(i >= 100 for i in phased_in_longest)
print('intervals in which longest phased block covered all variants:\t' + str(all_phased) + ' / ' + str(total_phasable) + ' (' + str(all_phased / float(total_phasable)) + ')')

# histogram of block counts per gene
plt.figure(0)
plt.hist(block_lengths, bins=range(min(block_lengths), max(block_lengths) + 1, 1))
plt.xlabel('number of blocks per gene')
plt.ylabel('count')
plt.savefig(args.output + '-block_lengths.pdf')

# histogram of fractions of variants phased in longest block
plt.figure(1)
plt.hist(phased_in_longest)
plt.xlabel('phased variants in longest block [%]')
plt.ylabel('count')
plt.savefig(args.output + '-longest_block.pdf')

# plot genes as function of how many variants are in largest block
x_values = []
y_values = []
for i in range(1,11):
	threshold = i * 10
	larger_than = sum(i >= threshold for i in phased_in_longest)
	y_value = larger_than / float(total_phasable)
	x_values.append(threshold)
	print(y_value * 100.0)
	y_values.append(y_value * 100.0)
plt.figure(2)
plt.plot(x_values, y_values, marker='o', linestyle='-')
plt.xlabel('phased variants in largest block (%)')
plt.ylabel('genes (%)')
plt.ylim(0,95)
plt.xticks(x_values)
plt.yticks([i*10 for i in range(0,10)])
plt.savefig(args.output + '-longest_block_cumulative.pdf')
