# Potato data

## Preprocessing

In the preprocessing step, the corrected minion reads are aligned to the potato reference genome. In order to run, the config-file must be adapted in the following way:

1. download potato reference genome () and add path to "reference" field in config file
2. set path to corrected reads ("correctedminion")
3. run Snakemake-preprocessing

## Phasing

The phasing pipeline can be run using the Snakefile contained in folder "phasing".

1. set paths to whatshap polyphase and snpeff in the Snakefile
2. run Snakefile
