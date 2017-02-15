#!/bin/bash

## Run the block below to get all the regions for the yield table
python make_stack_plot.py -v 'met_None' -o 'N'
python make_stack_plot.py -v 'met_Base' -o 'A'
python make_stack_plot.py -v 'met_Sym' -o 'A'
python make_stack_plot.py -v 'met_Op' -o 'A'
python make_stack_plot.py -v 'met_SRwJ' -o 'A'
python make_stack_plot.py -v 'met_SRnoJ' -o 'A'
