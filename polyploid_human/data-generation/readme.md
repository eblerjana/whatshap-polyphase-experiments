# Used input files

Reproducing the results requires three kinds of files:
1. Alignments (.bam) for the three human samples 'HG00514', 'HG00733' and 'NA19240'. These can be downloaded here: ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/hgsv_sv_discovery/working/20180102_pacbio_blasr_reheader/
2. One VCF-File for each sample, containing the heterozygous variants and the gold standard haplotypes, created by trio-based phasing. These are available on Zenodo (see paper for exact details)
3. A fastq-file (SRR3658380.fastq), which is used by the read simulator to generate reads with properties close to the original ones. It can be found here: https://www.ncbi.nlm.nih.gov/sra/SRX1837675

# Running the snakemake pipelines

The different test data are created using several runs of the provided snakemake pipeline. For tetraploid and hexaploid test data the snakefile 'Snakefile-polyploid-genome' has to be run with 'config.tetra.json' and 'config.hexa.json' provided as config files (line 3), respectively. For the pentaploid data, first run the same snakemake pipeline with 'config.penta.json' as config file. This will generate simulated hexaploid reads with coverage 48 and 96X (instead of 40 and 80X). Finally, run the 'Snakefile-hexa-to-penta' pipeline to filter out one haplotype from the generated reads, providing a pentaploid dataset with 40 and 80X.

Generating a pentaploid dataset from the real reads is a bit more involved, as we do not know the true haplotypes of these reads beforehand. One has to tag all reads in one diploid sample using the gold standard VCF file and the reads from one haplotype with the four haplotypes from the other two diploid samples.
