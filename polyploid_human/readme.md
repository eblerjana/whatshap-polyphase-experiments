# Used configurations for the publication:

The configurations might contain redundant runs, which should be recognized by snakemake.

## For the overview tables

"samples":["tetraploid","hexaploid"],
"methods":["polyphase_sens1","polyphase_sens4","hpop"]
"readtypes":["simulated","real"]

## For the comparison plots for different block cut sensitivies

"samples":["tetraploid"],
"methods":["polyphase_sens0","polyphase_sens1","polyphase_sens2","polyphase_sens3","polyphase_sens4","polyphase_sens5"]
"readtypes":["simulated","real"]

## For the pentaploid results

Leave out the results for real reads, because we did not generate them.

"samples":["pentaploid"],
"methods":["polyphase_sens1","polyphase_sens4","hpop"]
"readtypes":["simulated"]