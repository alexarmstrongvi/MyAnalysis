#!/bin/bash

# Run the block below to get all the regions for the yield table
python make_stack_plot.py -v 'met_None' -o 'W' 
python make_stack_plot.py -v 'met_Base' -o 'A' &
sleep 30
python make_stack_plot.py -v 'met_Sym' -o 'A' &
sleep 30
python make_stack_plot.py -v 'met_Op' -o 'A' &
sleep 30
python make_stack_plot.py -v 'met_SRwJ' -o 'A' &
sleep 30
python make_stack_plot.py -v 'met_SRnoJ' -o 'A' &
wait
python YieldTableMaker.py ../../../analysis_n0235_run/YieldTable_tmp.txt
rm ../../../analysis_n0235_run/tmp_LatexYieldTable.tex
echo "Done"

