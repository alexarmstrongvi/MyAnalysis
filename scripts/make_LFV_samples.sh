#!/bin/bash

python chain_process.py
echo
python check_for_failed_samples.py
echo
python print_failed_sample_stats.py
echo
hadd -f ../../../analysis_n0235_run/LFV.root ../../../analysis_n0235_run/samples/*root
