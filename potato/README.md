# Potato data

## Preprocessing

In the preprocessing step, the corrected minion reads are aligned to the potato reference genome. In order to run, the config-file must be adapted in the following way:

1. in the config file, set path to corrected reads ("correctedminion")
3. run: `` snakemake -s Snakefile-preprocessing ``

## Phasing

The phasing pipeline can be run using the Snakefile contained in folder "phasing".

1. set paths to whatshap polyphase and snpeff in the config file
2. run: `` snakemake ``
