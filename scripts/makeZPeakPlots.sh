#!/bin/bash

python make_stack_plot.py -v 'mll_SF' &
python make_stack_plot.py -v 'mll_mumu' &
python make_stack_plot.py -v 'mll_ee' &
python make_stack_plot.py -v 'mll_DF' &
wait
echo "Done with Plots"
