# Used configurations for the publication:

The different test data are created using several runs of the provided snakemake pipeline. For tetraploid and hexaploid test data the snakefile 'Snakefile-polyploid-genome' has to be run with 'config.tetra.json' and 'config.hexa.json' provided as config files (line 3), respectively. For the pentaploid data, first run the same snakemake pipeline with 'config.penta.json' as config file. This will generate simulated hexaploid reads with coverage 48 and 96X (instead of 40 and 80X). Finally, run the 'Snakefile-hexa-to-penta' pipeline to filter out one haplotype from the generated reads, providing a pentaploid dataset with 40 and 80X.

Generating a pentaploid dataset from the real reads is a bit more involved, as we do not know the true haplotypes of these reads beforehand. One has to tag all reads in one diploid sample using the gold standard VCF file and the reads from one haplotype with the four haplotypes from the other two diploid samples.
