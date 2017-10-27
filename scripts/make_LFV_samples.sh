#!/bin/bash

python chain_process.py
echo
python check_for_failed_samples.py
echo
python print_failed_sample_stats.py
