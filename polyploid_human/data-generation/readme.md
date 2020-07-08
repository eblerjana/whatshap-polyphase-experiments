# Used configurations for the publication:

The different test data are created using several runs of the provided snakemake pipeline. For tetraploid and hexaploid test data the snakefile 'Snakefile-polyploid-genome' has to be run with 'config-tetra.json' and 'config-hexa.json' provided as config files (line 3) respectively.

The pentaploid data is only available as a simulated dataset and downsamples from a hexaploid dataset. First, the hexaploid data has to be created via the 'Snakefile-polyploid-genome' pipeline using the 'config-hexa-to-penta.json' config. Second, the 'Snakefile-pentaploid-genome' pipeline has to be run.