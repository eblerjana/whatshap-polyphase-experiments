import sys

def hpopToVcfConverter(phasing_path, vcf_input_path, vcf_output_path):
	with open(phasing_path, 'r') as phasing_file, open(vcf_input_path, 'r') as vcf_input, open(vcf_output_path, 'w') as vcf_output:
		# Advance in hpop file until first phasing line is reached
		block_id = 0
		hpop_row = phasing_file.readline()
		while hpop_row != None and hpop_row.startswith("*"):
			hpop_row = phasing_file.readline()
		while hpop_row != None and hpop_row.startswith("BLOCK:"):
			block_id += 1
			hpop_row = phasing_file.readline()
		# Parse vcf row. If end of file reached, set row to -1.
		if (hpop_row.split("\t")[0]).isdigit():
			vcf_pos = int(hpop_row.split("\t")[0])
		else:
			vcf_pos = -1
		
		variant_row = 0 		# number of read non-header lines
		statistic_phased_vars = 0
		statistic_one_missing = 0
		statistic_more_missing = 0
		for row in vcf_input:
			#if hpop_row == None or vcf_pos < 0:
				# Reached end of phasing file
			#	break
			if row[0] == '#':
				# Header lines are just copied to output vcf
				vcf_output.write(row)
			else:
				variant_row += 1
				if variant_row == vcf_pos:
					# Copy vcf row, except the phasing information
					rowtabs = row.split("\t")
					next_output = "".join([tab+"\t" for tab in rowtabs[0:-1]])
					
					# Add phasing to vcf
					phasing = hpop_row.split("\n")[0].split("\t")[1:]
					phased_genotype = 0
					missing_entries = 0
					for p in phasing:
						if p.isdigit():
							phased_genotype += int(p)
						else:
							missing_entries += 1
					phasing_old = [p for p in phasing]
							
					# Look at missing entries
					if missing_entries == 0:
						# Phasing complete for current position
						next_output += "".join([p+"|" for p in phasing[:-1]])
						next_output += (phasing[-1] + ":" + str(block_id) + "\n")
						statistic_phased_vars += 1
					elif missing_entries == 1:
						# One haplotype missing. Try to infer from genotype
						real_genotype_list = rowtabs[-1].split(":")[0].replace("|", "/").split("/")
						real_genotype = sum([int(g) for g in real_genotype_list])
						diff = real_genotype - phased_genotype
						if 0 <= diff <= 1:
							for i in range(len(phasing)):
								if not phasing[i].isdigit():
									phasing[i] = str(diff)
									break
							next_output += "".join([p+"|" for p in phasing[:-1]])
							next_output += (phasing[-1] + ":" + str(block_id) + "\n")
							#print("Infer: "+str(phasing_old)+" -> "+str(phasing))
							statistic_one_missing += 1
						else:
							# Inference not possible. Omit position
							next_output += (rowtabs[-1].replace("|", "/"))
							#print("Infer: "+str(phasing_old)+" -> n/a : "+rowtabs[-1].replace("|", "/"))
							statistic_more_missing += 1
					else:
						# Too many haplotypes missing. Omit position
						next_output += (rowtabs[-1].replace("|", "/"))
						#print("Missing: "+str(phasing_old)+" -> n/a : "+rowtabs[-1].replace("|", "/"))
						statistic_more_missing += 1
						
					vcf_output.write(next_output)
					
					# Advance in hpop file until next phasing line is reached
					hpop_row = phasing_file.readline()
					while hpop_row != None and hpop_row.startswith("*"):
						hpop_row = phasing_file.readline()
					while hpop_row != None and hpop_row.startswith("BLOCK:"):
						block_id += 1
						hpop_row = phasing_file.readline()
					# Parse vcf row. If end of file reached, set row to -1.
					if (hpop_row.split("\t")[0]).isdigit():
						vcf_pos = int(hpop_row.split("\t")[0])
					else:
						vcf_pos = -1

				else:
					# No phasing information for this line. Copy vcf row, but delete existent phasing, only keep genotype
					rowtabs = row.split("\t")
					next_output = "".join([tab+"\t" for tab in rowtabs[0:-1]])
					next_output += (rowtabs[-1].replace("|", "/"))
					vcf_output.write(next_output)

	total = statistic_phased_vars + statistic_one_missing + statistic_more_missing
	print("Parsed "+str(block_id)+" blocks with a total of "+str(total)+" variants, from which "+str(statistic_phased_vars)+" are completely phased, "+str(statistic_one_missing)+" could be infered from genotype information and "+str(statistic_more_missing)+" are unphased.")

def main(argv):
	if (len(argv) != 4):
		print("Required call format:")
		print("python hpop2vcf.py <hpop-file> <input-vcf> <output-vcf>")
	else:
		hpopToVcfConverter(argv[1], argv[2], argv[3])
	
if __name__ == '__main__':
	main(sys.argv)